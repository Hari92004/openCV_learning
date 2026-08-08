import sys
print(f"Python: {sys.version}")
print(f"Prefix: {sys.prefix}")

try:
    import mediapipe as mp
    print(f"MediaPipe Version: {mp.__version__}")
    print(f"MediaPipe File: {mp.__file__}")
except Exception as e:
    print(f"Import Error: {e}")

print("\n--- Testing Imports ---")

try:
    import mediapipe.solutions.hands as hands
    print("SUCCESS: import mediapipe.solutions.hands as hands")
except Exception as e:
    print(f"FAILED: import mediapipe.solutions.hands as hands -> {e}")

try:
    from mediapipe.python.solutions import hands
    print("SUCCESS: from mediapipe.python.solutions import hands")
except Exception as e:
    print(f"FAILED: from mediapipe.python.solutions import hands -> {e}")

try:
    import mediapipe.python.solutions.hands as hands
    print("SUCCESS: import mediapipe.python.solutions.hands as hands")
except Exception as e:
    print(f"FAILED: import mediapipe.python.solutions.hands as hands -> {e}")
