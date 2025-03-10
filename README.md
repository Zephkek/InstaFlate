# CVE Report: Instagram Denial-of-Service via Malformed Drawable Resource

## Summary
A memory exhaustion vulnerability has been identified in Instagram for Android (versions ≤ 370.1.0.43.96), which leads to application termination due to improper handling of malformed drawable resources in end-to-end encrypted (E2EE) group chats. When a user attempts to 'like' a message referencing a non-existent or corrupted drawable resource, the application enters an infinite retry allocation state, ultimately causing an **OutOfMemoryError (OOM)** and resulting in a forced crash.

## Vulnerability Details

### **Vulnerability Type**
Denial-of-Service (DoS) via Heap Exhaustion triggered by improper drawable resource handling.

### **Root Cause**
Instagram's Android application fails to properly handle corrupted or missing drawable resources, leading to repeated allocation attempts that rapidly exhaust heap memory.

### **Crash Chain Analysis**
1. **Malformed drawable resource is referenced** (e.g., ID: `0x7f0802d7`).
2. **Android attempts repeated allocations**, unable to locate the resource.
3. **Garbage collection cycles fail to free sufficient heap space**.
4. **App crashes due to `java.lang.OutOfMemoryError`**.
5. **User interface thread stalls, triggering an ANR (Application Not Responding)**.
6. **Instagram is forcibly terminated by the OS after ~10 seconds**.

## Proof of Concept (PoC)

### **Reproduction Steps**
1. **Create an E2EE Group Chat**
   - Start a group chat on Instagram with end-to-end encryption enabled.
2. **Exchange Messages**
   - Participants send text and voice messages in the chat.
3. **Trigger the Exploit**
   - A participant attempts to 'like' a message containing the malformed drawable resource.
4. **Observe the Impact**
   - Instagram crashes on all devices that render the affected message.

### **PoC Reproduction Conditions**
- Instagram for Android **≤ 370.1.0.43.96**.
- Device running **Android OS**.
- **E2EE-enabled group chat**.

### **Observed Impact**
- **Severity**: High (Denial-of-Service for all affected group participants).
- **Scope**: Any user who views or interacts with the malformed message experiences repeated app crashes.

### **Crash Summary**
The application (`com.instagram.android`) crashes due to an **OutOfMemoryError**:

```
java.lang.OutOfMemoryError: Failed to allocate a 83070912 byte allocation with 2719552 free bytes and 2655KB until OOM, target footprint 536870912, growth limit 536870912
```

**Crash Occurrence:**
```
03-10 15:49:18.549 PID:7226 Thread:SWPool3_t1of1
```

### **Stack Trace Analysis**
The failure occurs due to excessive memory allocation within Instagram’s internal class structures:

```
at java.util.Arrays.copyOf(Arrays.java:3553)
at java.util.ArrayList.grow(ArrayList.java:244)
at java.util.ArrayList.add(ArrayList.java:461)
at X.057T.<init>(:13)
at X.0NrL.E4V(:8)
at X.0Jqg.run(:8)
```

### **Memory Spike and Heap Exhaustion**
Using `adb_memory_monitor.py`, the following memory pattern was observed before the crash:

| Timestamp  | Java Heap (MB) | Native Heap (MB) | Total PSS (MB) |
|------------|--------------|----------------|--------------|
| 15:48:06   | 26.38        | 31.16          | 189.52       |
| 15:48:10   | 23.69        | 30.79          | 188.17       |
| 15:48:16   | 49.21        | 74.66          | 307.69       |
| 15:48:25   | 55.42        | 133.26         | 543.30       |
| 15:48:34   | 87.61        | 107.73         | 576.12       |
| 15:48:37   | 313.38       | 114.01         | 831.76       |
| 15:48:45   | 510.41       | 170.91         | 1118.22      |
| 15:48:49   | 527.47       | 160.32         | 1133.10      |
| 15:49:13   | 527.22       | 95.01          | 1077.53      |
| 15:49:19   | 527.23       | 96.95          | 1079.59      |
| **15:49:25** | **Crash Occurs** | **Application Terminates** |

### Video POC showing this in real time:

https://github.com/user-attachments/assets/c1d0ee7e-47ef-4481-8052-51674d777c6f

### **Associated Errors**
- **`Resources$NotFoundException`** occurs multiple times for missing drawable assets (`instagram_arrow_left_outline_24`, `tab_direct_drawable`, `instagram_heart_outline_24`, etc.).
- **ANR Incidents** observed for Instagram's `ModalActivity` and input method failures (`com.samsung.android.honeyboard`).

## **Exploit Demonstration**
- **Video Proof of Concept:** _(Memory exhaustion and forced app crash)_
  - (Impact on Galaxy A52 group participant 1)
    
   https://github.com/user-attachments/assets/93002dd6-77dd-4b7f-b2fd-5ba86372f588
  
  - (Impact on S22U 12Gb ram, group participant 2)
    
   https://github.com/user-attachments/assets/8281d960-0493-4849-bcad-3475103719a3
  
  -  (Impact on group participant 3 Infinix Note 40 Pro+ 12gb ram.)
    
   https://github.com/user-attachments/assets/57e1904d-370f-40b1-baa6-efc3f30655e0

## **Mitigation & Recommendations**
1. **Robust Resource Validation**: Ensure drawable resources are verified and available before rendering.
2. **Graceful Exception Handling**: Catch and handle `ResourceNotFoundException` errors without triggering repeated allocation attempts.
3. **Isolated Execution Environment**: Process drawable inflation in sandboxed threads with strict memory limits.
4. **Heap Protection**: Implement **memory allocation caps** to prevent excessive memory consumption when handling missing resources.

## **Disclosure Timeline**
- **Initial Report**: 2025-03-08
- **CNA Notification**: 2025-03-09
- **Public Disclosure**: TBD (pending responsible disclosure protocols)
