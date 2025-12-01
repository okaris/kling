# Kling AI Authentication

The Kling AI API uses **Access Key** and **Secret Key** authentication.

## Getting Your Credentials

1. Visit the [Kling AI Console](https://klingai.com)
2. Navigate to **API Settings** or **API Keys**
3. Generate or retrieve your credentials:
   - **Access Key** (starts with `ak-`)
   - **Secret Key** (keep this secure!)

## Authentication Methods

### Method 1: Direct Initialization

```python
from kling import KlingClient

client = KlingClient(
    access_key="ak-your-access-key",
    secret_key="your-secret-key"
)
```

### Method 2: Environment Variables (Recommended)

**1. Set environment variables:**

```bash
export KLING_ACCESS_KEY="ak-your-access-key"
export KLING_SECRET_KEY="your-secret-key"
```

**2. Use in your code:**

```python
import os
from kling import KlingClient

client = KlingClient(
    access_key=os.getenv("KLING_ACCESS_KEY"),
    secret_key=os.getenv("KLING_SECRET_KEY")
)
```

### Method 3: .env File

**1. Create `.env` file:**

```bash
KLING_ACCESS_KEY=ak-your-access-key
KLING_SECRET_KEY=your-secret-key
```

**2. Load with python-dotenv:**

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os
from kling import KlingClient

load_dotenv()  # Load .env file

client = KlingClient(
    access_key=os.getenv("KLING_ACCESS_KEY"),
    secret_key=os.getenv("KLING_SECRET_KEY")
)
```

## How It Works

The SDK sends your credentials in the HTTP headers:

```http
POST /v1/videos/text2video HTTP/1.1
Host: api-singapore.klingai.com
X-Api-Key: ak-your-access-key
X-Api-Secret: your-secret-key
Content-Type: application/json
```

## Security Best Practices

1. **Never commit credentials to version control**
   - Add `.env` to `.gitignore`
   - Use environment variables in production

2. **Rotate keys regularly**
   - Generate new keys periodically
   - Revoke old keys when no longer needed

3. **Use different keys for different environments**
   - Development keys for testing
   - Production keys for live applications

4. **Limit key permissions**
   - Only grant necessary permissions
   - Monitor API usage for anomalies

## Troubleshooting

### "Authentication failed" error

**Problem:** Your access key or secret key is invalid.

**Solution:**
1. Verify your keys in the Kling AI Console
2. Ensure there are no extra spaces or newlines
3. Check that the access key starts with `ak-`

### "Missing credentials" error

**Problem:** Access key or secret key not provided.

**Solution:**
```python
# Make sure both are set
assert os.getenv("KLING_ACCESS_KEY"), "KLING_ACCESS_KEY not set"
assert os.getenv("KLING_SECRET_KEY"), "KLING_SECRET_KEY not set"
```

### Headers not being sent

**Problem:** Custom HTTP client or proxy interfering.

**Solution:**
The SDK automatically adds these headers:
- `X-Api-Key`: Your access key
- `X-Api-Secret`: Your secret key
- `Content-Type`: application/json

If using a custom proxy, ensure it forwards these headers.

## Regional Endpoints

You can specify different base URLs for different regions:

```python
# Singapore (default)
client = KlingClient(
    access_key="ak-xxx",
    secret_key="xxx",
    base_url="https://api-singapore.klingai.com"
)

# Or use environment variable
export KLING_BASE_URL="https://api-singapore.klingai.com"
```

## Rate Limiting

Kling AI enforces rate limits based on your account tier. The SDK does not automatically handle rate limiting, but you can:

1. **Check response headers** for rate limit info
2. **Implement retry logic** with exponential backoff
3. **Monitor your usage** via the Kling AI Console

Example with retry:

```python
import time
from kling import KlingClient, KlingAPIError

client = KlingClient(access_key="...", secret_key="...")

max_retries = 3
for attempt in range(max_retries):
    try:
        task = client.text_to_video.create(prompt="...")
        break
    except KlingAPIError as e:
        if e.code == 429:  # Rate limit error
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
        else:
            raise
```

## Questions?

- Check the [Kling AI API Documentation](https://docs.klingai.com)
- Visit the [Kling AI Console](https://klingai.com)
- Open an issue on GitHub
