# batch_key_tester_full.py
import re
from openai import OpenAI
from tqdm import tqdm

def validate_key(key):
    """Comprehensive API key validator"""
    try:
        # Format validation
        if not re.match(r"^sk-[a-zA-Z0-9]{48}$", key):
            return "❌ Invalid Format"
        
        # API functionality test
        client = OpenAI(api_key=key)
        client.models.list()  # Actual API call
        return "✅ Valid Key"
        
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            return "❌ Invalid Key (401)"
        return f"❌ API Error: {error_msg[:50]}..."

def test_keys(keys):
    """Batch test multiple keys with progress tracking"""
    results = {}
    for key in tqdm(keys, desc="Validating Keys"):
        results[key] = validate_key(key)
    return results

def mask_key(key):
    """Secure key masking for output"""
    if len(key) < 12:
        return "*****"
    return key[:6] + "****" + key[-4:]

if __name__ == "__main__":
    # Full list of keys to test
    keys = [
        "sk-abcdef1234567890abcdef1234567890abcdef12",
        "sk-1234567890abcdef1234567890abcdef12345678",
        "sk-abcdefabcdefabcdefabcdefabcdefabcdef12",
        "sk-7890abcdef7890abcdef7890abcdef7890abcd",
        "sk-1234abcd1234abcd1234abcd1234abcd1234abcd",
        "sk-abcd1234abcd1234abcd1234abcd1234abcd1234",
        "sk-5678efgh5678efgh5678efgh5678efgh5678efgh",
        "sk-efgh5678efgh5678efgh5678efgh5678efgh5678",
        "sk-ijkl1234ijkl1234ijkl1234ijkl1234ijkl1234",
        "sk-mnop5678mnop5678mnop5678mnop5678mnop5678",
        "sk-qrst1234qrst1234qrst1234qrst1234qrst1234",
        "sk-uvwx5678uvwx5678uvwx5678uvwx5678uvwx5678",
        "sk-1234ijkl1234ijkl1234ijkl1234ijkl1234ijkl",
        "sk-5678mnop5678mnop5678mnop5678mnop5678mnop",
        "sk-qrst5678qrst5678qrst5678qrst5678qrst5678",
        "sk-uvwx1234uvwx1234uvwx1234uvwx1234uvwx1234",
        "sk-1234abcd5678efgh1234abcd5678efgh1234abcd",
        "sk-5678ijkl1234mnop5678ijkl1234mnop5678ijkl",
        "sk-abcdqrstefghuvwxabcdqrstefghuvwxabcdqrst",
        "sk-ijklmnop1234qrstijklmnop1234qrstijklmnop",
        "sk-1234uvwx5678abcd1234uvwx5678abcd1234uvwx",
        "sk-efghijkl5678mnopabcd1234efghijkl5678mnop",
        "sk-mnopqrstuvwxabcdmnopqrstuvwxabcdmnopqrst",
        "sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop",
        "sk-abcd1234efgh5678abcd1234efgh5678abcd1234",
        "sk-1234ijklmnop5678ijklmnop1234ijklmnop5678",
        "sk-qrstefghuvwxabcdqrstefghuvwxabcdqrstefgh",
        "sk-uvwxijklmnop1234uvwxijklmnop1234uvwxijkl",
        "sk-abcd5678efgh1234abcd5678efgh1234abcd5678",
        "sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop",
        "sk-1234qrstuvwxabcd1234qrstuvwxabcd1234qrst",
        "sk-efghijklmnop5678efghijklmnop5678efghijkl",
        "sk-mnopabcd1234efghmnopabcd1234efghmnopabcd",
        "sk-ijklqrst5678uvwxijklqrst5678uvwxijklqrst",
        "sk-1234ijkl5678mnop1234ijkl5678mnop1234ijkl",
        "sk-abcdqrstefgh5678abcdqrstefgh5678abcdqrst",
        "sk-ijklmnopuvwx1234ijklmnopuvwx1234ijklmnop",
        "sk-efgh5678abcd1234efgh5678abcd1234efgh5678",
        "sk-mnopqrstijkl5678mnopqrstijkl5678mnopqrst",
        "sk-1234uvwxabcd5678uvwxabcd1234uvwxabcd5678",
        "sk-ijklmnop5678efghijklmnop5678efghijklmnop",
        "sk-abcd1234qrstuvwxabcd1234qrstuvwxabcd1234",
        "sk-1234efgh5678ijkl1234efgh5678ijkl1234efgh",
        "sk-5678mnopqrstuvwx5678mnopqrstuvwx5678mnop",
        "sk-abcdijkl1234uvwxabcdijkl1234uvwxabcdijkl",
        "sk-ijklmnopabcd5678ijklmnopabcd5678ijklmnop",
        "sk-1234efghqrstuvwx1234efghqrstuvwx1234efgh",
        "sk-5678ijklmnopabcd5678ijklmnopabcd5678ijkl",
        "sk-abcd1234efgh5678abcd1234efgh5678abcd1234",
        "sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop"
    ]
    
    print("Starting Batch Validation...\n")
    results = test_keys(keys)
    
    print("\nValidation Report:")
    print(f"{'Key':<40} {'Status':<20}")
    print("-" * 60)
    
    valid_count = 0
    invalid_count = 0
    
    for key, status in results.items():
        print(f"{mask_key(key):<40} {status:<20}")
        if "✅" in status:
            valid_count += 1
        else:
            invalid_count += 1
    
    print("\nSummary:")
    print(f"Valid Keys: {valid_count}")
    print(f"Invalid Keys: {invalid_count}")
    print(f"Success Rate: {valid_count/(valid_count+invalid_count)*100:.1f}%")
