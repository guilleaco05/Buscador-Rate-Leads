# Example: Echo Test

## Goal
Demonstrate the DOE system with a simple echo test that validates the directive → execution flow.

## Inputs
- `message`: A text string to echo back
- `repeat_count`: (Optional) Number of times to repeat the message (default: 1)

## Execution
Run the script:
```bash
python execution/example_echo.py --message "Hello DOE" --repeat 3
```

## Outputs
- Console output showing the echoed message
- A temporary file in `.tmp/echo_output.txt` containing the result

## Edge Cases
- **Empty message**: Script should handle gracefully with a warning
- **Invalid repeat count**: Should default to 1 and log a warning
- **File write errors**: Should still output to console even if file write fails

## Learnings
(This section will be updated as we discover constraints or improvements)

- Initial version created as demonstration
