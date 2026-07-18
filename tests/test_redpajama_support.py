import unittest
from types import SimpleNamespace
from unittest.mock import patch

from llava.model import builder


class _DummyTokenizer:
    def __init__(self):
        self._size = 1000

    def add_tokens(self, tokens, special_tokens=False):
        self._size += len(tokens)

    def __len__(self):
        return self._size


class _DummyVisionTower:
    def __init__(self):
        self.is_loaded = True
        self.image_processor = object()

    def load_model(self, device_map="auto"):
        self.is_loaded = True

    def to(self, device=None, dtype=None):
        return self


class _DummyModel:
    def __init__(self):
        self.config = SimpleNamespace(
            mm_use_im_start_end=False,
            mm_use_im_patch_token=False,
            max_sequence_length=4096,
        )
        self._vision_tower = _DummyVisionTower()

    def resize_token_embeddings(self, size):
        return size

    def get_vision_tower(self):
        return self._vision_tower


class TestRedPajamaModelNameDetection(unittest.TestCase):
    def test_detects_redpajama(self):
        self.assertTrue(builder._is_redpajama_model_name("RedPajama-INCITE-3B-v1"))

    def test_detects_gpt_neox_alias(self):
        self.assertTrue(builder._is_redpajama_model_name("my-gpt-neox-backbone"))

    def test_non_redpajama_model_returns_false(self):
        self.assertFalse(builder._is_redpajama_model_name("llava-v1.5-7b"))


class TestBuilderRoutingForRedPajama(unittest.TestCase):
    @patch("llava.model.builder.LlavaGptNeoXForCausalLM.from_pretrained")
    @patch("llava.model.builder.AutoTokenizer.from_pretrained")
    def test_llava_redpajama_loads_gpt_neox_llava_model(self, mock_tokenizer_from_pretrained, mock_llava_neox_from_pretrained):
        mock_tokenizer_from_pretrained.return_value = _DummyTokenizer()
        mock_llava_neox_from_pretrained.return_value = _DummyModel()

        builder.load_pretrained_model(
            model_path="/tmp/llava-redpajama",
            model_base=None,
            model_name="llava-redpajama-3b",
            device="cpu",
        )

        self.assertTrue(mock_llava_neox_from_pretrained.called)
        _, kwargs = mock_llava_neox_from_pretrained.call_args
        self.assertTrue(kwargs["low_cpu_mem_usage"])
        self.assertTrue(kwargs["trust_remote_code"])

    @patch("llava.model.builder.AutoModelForCausalLM.from_pretrained")
    @patch("llava.model.builder.AutoTokenizer.from_pretrained")
    def test_language_only_redpajama_uses_auto_model_with_remote_code(self, mock_tokenizer_from_pretrained, mock_auto_model_from_pretrained):
        mock_tokenizer_from_pretrained.return_value = _DummyTokenizer()
        mock_auto_model_from_pretrained.return_value = SimpleNamespace(
            config=SimpleNamespace(max_sequence_length=2048)
        )

        builder.load_pretrained_model(
            model_path="/tmp/redpajama",
            model_base=None,
            model_name="redpajama-3b",
            device="cpu",
        )

        _, tok_kwargs = mock_tokenizer_from_pretrained.call_args
        self.assertTrue(tok_kwargs["use_fast"])
        self.assertTrue(tok_kwargs["trust_remote_code"])

        _, model_kwargs = mock_auto_model_from_pretrained.call_args
        self.assertTrue(model_kwargs["trust_remote_code"])


if __name__ == "__main__":
    unittest.main()
