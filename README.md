# Boring Metrics Python SDK

This is a Python SDK for the Boring Metrics API. It provides a simple and efficient way to interact with the API from your Python applications.

## Installation

```bash
pip install boringmetrics
```

## Usage

### Basic Usage

```python
from boringmetrics import BoringMetrics

# Initialize the SDK
BoringMetrics.initialize("YOUR_API_TOKEN")

# Send a log
BoringMetrics.get_instance().logs.send(
    type="log",
    level="info",
    message="User signed in",
    data={"userId": "123"}
)

# Send multiple logs
BoringMetrics.get_instance().logs.send_batch([
    {"type": "log", "level": "warn", "message": "Something looks weird"},
    {"type": "log", "level": "error", "message": "Something broke!", "data": {"error": "Connection timeout"}}
])

# Set a live metric value
BoringMetrics.get_instance().lives.update(
    liveId="metric-123",
    value=42,
    operation="set"
)

# Increment a live metric value
BoringMetrics.get_instance().lives.update(
    liveId="metric-123",
    value=5,
    operation="increment"
)
```

### Alternative Syntax

You can also use a more concise syntax after initialization:

```python
from boringmetrics import BoringMetrics

# Initialize the SDK
bm = BoringMetrics.initialize("YOUR_API_TOKEN")

# Send a log
bm.logs.send(
    type="log",
    level="info",
    message="User signed in",
    data={"userId": "123"}
)

# Set a live metric value
bm.lives.update(
    liveId="metric-123",
    value=42,
    operation="set"
)
```

### Configuration Options

You can customize the SDK behavior with configuration options:

```python
BoringMetrics.initialize(
    "YOUR_API_TOKEN",
    maxRetryAttempts=3,
    logsMaxBatchSize=50,
    logsSendInterval=10,  # seconds
    livesMaxBatchSize=10,
    livesDebounceTime=2   # seconds
)
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/boringmetrics/python-sdk.

## Contributors

Thanks to everyone who contributed to the Boring Metrics Python SDK!

<a href="https://github.com/boringmetrics/python-sdk/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=boringmetrics/python-sdk" />
</a>

## License

The package is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
