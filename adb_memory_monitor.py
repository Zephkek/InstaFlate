# Instagram Denial-of-Service via Malformed Drawable Resource

## Summary
A memory exhaustion vulnerability exists in Instagram for Android (versions ≤ 370.1.0.43.96) due to improper handling of malformed drawable resources in end-to-end encrypted (E2EE) group chats. Specifically, attempting to 'like' a message referencing a non-existent or corrupted drawable triggers infinite retry allocations, causing OutOfMemoryError (OOM) and resulting in app termination.

## Technical Details

### Vulnerability Type:
Denial-of-Service (DoS) via Heap Exhaustion caused by improper handling of malformed drawable resources.

### Root Cause:
Instagram's Android app lacks adequate validation for drawable resources, leading to repeated and unsuccessful memory allocation attempts upon encountering corrupted or invalid drawable references, ultimately exhausting heap memory.

### Crash Chain Analysis:
- Reference to malformed drawable resource (e.g., invalid ID: `0x7f0802d7`).
- Repeated unsuccessful memory allocation attempts by Android.
- Excessive garbage collection cycles fail to reclaim sufficient memory.
- Heap exhaustion results in `java.lang.OutOfMemoryError`.
- UI thread stalls, causing an Application Not Responding (ANR) condition.
- Instagram app forcibly terminated by OS after approximately 10 seconds.

### Reproduction Steps:

1. **Establish E2EE Group Chat**:
   - Start an end-to-end encrypted group conversation on Instagram.

2. **Inject Malicious Message**:
   - Craft or send a message referencing an invalid or corrupted drawable resource (e.g., corrupted emoticon or sticker).

3. **Execute Exploit**:
   - A participant attempts to 'like' the maliciously crafted message.

4. **Verify Impact**:
   - All clients rendering the affected 'like' attempt experience repeated memory allocations, resulting in OOM errors and subsequent app crashes.

### PoC Conditions:
- Instagram Android version ≤ 370.1.0.43.96
- Android devices
- End-to-end encryption enabled for Instagram group chat

### Impact:
- **Severity**: High (Denial-of-Service)
- **Scope**: All participants viewing or interacting with the malicious message

### Video Proof-of-Concept (PoC):

#### Device 1: Galaxy A52 (E2EE enabled)

https://github.com/user-attachments/assets/93002dd6-77dd-4b7f-b2fd-5ba86372f588

![Device 1 Crash](https://github.com/user-attachments/assets/d81af352-284c-486a-b8d8-47eb7a142f6e)

#### Device 2: Galaxy Android Device

![Device 2 Crash](https://github.com/user-attachments/assets/8281d960-9e7d-43f1-837f-324af3b2f41d)

### Crash Monitoring Data

```
Monitoring memory usage for com.instagram.android

Time             Java Heap     Native Heap       Total PSS
==================================================
[15:48:06] Java: 26.38 MB | Native: 31.16 MB | Total: 189.52 MB
[15:48:07] Java: 23.69 MB | Native: 30.79 MB | Total: 188.23 MB
...
[15:48:37] Java: 313.38 MB | Native: 114.01 MB | Total: 427.39 MB
[15:48:37] Java: 510.41 MB | Native: 118.66 MB | Total: 629.07 MB
[15:49:19] Java: 527.23 MB | Native: 96.95 MB | Total: 1079.59 MB
[15:49:25] Java: N/A MB | Native: N/A MB | Total: N/A MB (Crash)
```

### Mitigation Recommendations:
- **Resource Validation**: Implement strict validation checks for drawable resources to prevent corrupted or invalid data from causing repeated allocation attempts.
- **Exception Handling**: Employ robust exception handling mechanisms to catch errors such as `OutOfMemoryError` and `ResourceNotFoundException`, preventing continuous retry attempts.
- **Isolated Execution**: Perform drawable rendering and resource allocation within isolated or sandboxed threads/environments with strict resource limitations to prevent application-wide impact.

### Disclosure Timeline:
- **Initial Report**: 03/08/2025
- **CNA Notification**: 03/09/2025
- **Public Disclosure**: Pending
```

