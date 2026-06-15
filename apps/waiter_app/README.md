# Waiter Android App

Flutter Android application planned for waiter-facing voice order capture.

## Current state

This directory is intentionally a skeleton for TASK T-001. No Flutter project has been generated yet.

## Intended responsibilities

- Authenticate waiter users.
- Show restaurant table list and open table orders.
- Capture voice commands after explicit waiter action.
- Display AI/STT/parser output as an editable draft.
- Require human confirmation before any order item is submitted.
- Show table order history and close-order flow.

## Stack boundary

- Target stack: Flutter for Android.
- Do not add platform-specific microphone or build configuration before the Flutter bootstrap task defines versions and permissions.
