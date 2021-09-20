# Tests for API

## Integration tests

Integration tests use Python3 along with `unittest` library. To run tests do the following:

1. Run the server

```bash
$ bundle exec rackup
```

2. Run all the tests from console

```bash
python3 -m unittest discover -s tests/integration/
```