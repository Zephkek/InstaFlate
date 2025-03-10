# Instagram Denial-of-Service via Malformed Drawable Resource

## Summary
A memory exhaustion vulnerability exists in Instagram for Android (versions ≤ 370.1.0.43.96) due to improper handling of malformed drawable resources in end-to-end encrypted (E2EE) group chats. Specifically, attempting to 'like' a message referencing a non-existent or corrupted drawable triggers infinite retry allocations, causing OutOfMemoryError (OOM) and app termination.

## Technical Details

### Vulnerability Type:
Denial-of-Service (DoS) via Heap Exhaustion triggered by malformed drawable resource handling.

### Root Cause:
Instagram's Android app fails to handle corrupted drawable resources safely, leading to repeated unsuccessful allocations that exhaust heap memory.

### Crash Chain Analysis:
- Malformed drawable resource referenced (e.g., ID: `0x7f0802d7`)
- Android attempts to allocate memory repeatedly
- Rapid garbage collection cycles unable to free adequate heap space
- Leads to `java.lang.OutOfMemoryError`
- App UI thread stalls, causing an ANR (Application Not Responding)
- Instagram app forcibly terminated by the OS after ~10 seconds.

### Reproduction Steps:

1. **Create E2EE Group Chat**:
   - Initiate an end-to-end encrypted group chat on Instagram.

2. **Malicious Message Injection**:
   - Craft or send a message that references a non-existent drawable resource (e.g., an emoticon/sticker with corrupted or invalid ID).

3. **Trigger Exploit**:
   - A group member attempts to 'like' the malicious message.

4. **Observe Effect**:
   - All group chat clients that render the 'like' experience repeated memory allocations, OOM errors, and app crashes.

### PoC Reproduction Conditions:
- Instagram Android ≤ 370.1.0.43.96
- Android device
- E2EE enabled Instagram group chat

### Impact:
- **Severity**: High (Denial-of-Service)
- **Scope**: All participants viewing/interacting with the malformed message
### Video POC of imapct on multiple devices in group:

# Device 1 (User one in group OK with end to end enc enabled Galaxy A52)

https://github.com/user-attachments/assets/93002dd6-77dd-4b7f-b2fd-5ba86372f588

![20250310_135134](https://github.com/user-attachments/assets/d81af352-284c-486a-b8d8-47eb7a142f6e)

# Device 2 (User 2 in group in group OK with end to end enc enabled Galaxy S22 Ultra)

https://github.com/user-attachments/assets/8281d960-0493-4849-bcad-3475103719a3

### Mitigation Recommendations:
- **Robust Resource Validation**: Ensure drawable resources are verified before rendering.
- **Graceful Exception Handling**: Catch exceptions like `ResourceNotFoundException` and handle gracefully without repeated allocation attempts.
- **Isolated Execution Environment**: Process drawable inflation in isolated/sandboxed threads with strict memory limits.

### Disclosure Timeline:
- **Initial Report**: 03/08/2025
- **CNA Notification**: 03/09/2025
- **Public Disclosure**: TBD (following responsible disclosure guidelines)

