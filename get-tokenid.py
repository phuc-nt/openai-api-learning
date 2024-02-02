from transformers import GPT2TokenizerFast

# Initialize the tokenizer for gpt-3.5-turbo
tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/gpt-3.5-turbo')

# Tokenize a word or phrase
tokens = tokenizer.tokenize("Fu")

# Convert tokens to token IDs
token_ids = tokenizer.convert_tokens_to_ids(tokens)

print("Tokens:", tokens)
print("Token IDs:", token_ids)