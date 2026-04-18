import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ModelLoader:
    """Handles loading and inference with the AI model"""
    
    _instance: Optional['ModelLoader'] = None
    _model = None
    _tokenizer = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one model instance"""
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def load_model(self, model_name: str = "gpt2", device: str = "cpu"):
        """
        Load tokenizer and model from Hugging Face
        
        Args:
            model_name: Model identifier from Hugging Face (default: gpt2)
            device: Device to load model on (cpu or cuda)
        """
        if self._model is None:
            try:
                logger.info(f"Loading model: {model_name}")
                self._tokenizer = GPT2Tokenizer.from_pretrained(model_name)
                self._model = GPT2LMHeadModel.from_pretrained(model_name)
                self._model.to(device)
                self._model.eval()
                logger.info(f"Model loaded successfully on {device}")
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise
    
    def generate_story(self, prompt: str, max_length: int = 200, device: str = "cpu") -> str:
        """
        Generate story based on prompt
        
        Args:
            prompt: Input prompt for story generation
            max_length: Maximum length of generated story
            device: Device to use for inference
            
        Returns:
            Generated story text
        """
        if self._model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        try:
            input_ids = self._tokenizer.encode(prompt, return_tensors="pt").to(device)
            
            with torch.no_grad():
                output = self._model.generate(
                    input_ids,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self._tokenizer.eos_token_id
                )
            
            story = self._tokenizer.decode(output[0], skip_special_tokens=True)
            return story
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            raise
    
    @property
    def model(self):
        return self._model
    
    @property
    def tokenizer(self):
        return self._tokenizer


# Singleton instance
model_loader = ModelLoader()
