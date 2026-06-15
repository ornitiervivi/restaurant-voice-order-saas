# Flutter compatibility

## Project scope

Flutter governs the Android waiter app and may govern the web/admin/kitchen/bar interfaces through Flutter Web when that choice is confirmed.

## Required checks before implementation

- Confirm current stable Flutter and Dart versions for the development environment.
- Confirm Android SDK, minimum Android version, microphone permission flow and build target.
- Confirm whether admin/kitchen/bar screens use Flutter Web or an equivalent frontend.
- Validate browser support if Flutter Web is selected.
- Validate package compatibility for audio recording, state management, routing, HTTP and WebSocket clients.

## Constraints

- The waiter app must show a human confirmation screen before any parsed voice order is submitted.
- UI flows must preserve edit/review actions for ambiguous or low-confidence parsed commands.
- Avoid platform-specific code until the Android requirements and permissions are confirmed.
