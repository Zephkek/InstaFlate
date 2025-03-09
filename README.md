
# Instagram Denial-of-Service via Malformed Drawable Resource

## **Summary**
A memory exhaustion vulnerability exists in Instagram for Android (versions ≤ 370.1.0.43.96) due to improper handling of malformed drawable resources in group chats. Processing a specially crafted drawable triggers infinite allocation loops, cascading exceptions, and heap exhaustion, leading to forced application termination (DoS) for all users who view the malicious message.

## **Technical Details**
### **Affected Versions**
- Instagram for Android ≤ 370.1.0.43.96

### **Vulnerability Type**
- Denial-of-Service (DoS) via Resource-Induced Heap Exhaustion

### **Root Cause**
The app fails to validate drawable resources before inflation. When a malformed or missing drawable (referenced by static IDs like `0x7f0802d7`, `0x7f020004`) is processed, background threads (e.g., `IgExecutorV2`, `SWPool3_t1of1`) enter an infinite retry loop, attempting to allocate trivial amounts of memory (16–32 bytes) while generating unhandled `ResourceNotFoundException` and `NullPointerException` errors.

### **Crash Chain Analysis**
1. **Memory Exhaustion**  
   - Failed allocations due to rapid garbage collection (GC) cycles:  
     ```
     FATAL EXCEPTION: IgExecutorV2 #321  
     OutOfMemoryError: Failed to allocate 16 bytes (free: 269152 bytes, heap target: 536MB)  
     ```  
   - Subsequent failures in other threads (e.g., `SWPool3_t1of1` for 32-byte allocations).  

2. **Exception Cascade**  
   - `ResourceNotFoundException` for unresolved drawables (e.g., `#0x7f0802d7`).  
   - `NullPointerException` in critical methods (e.g., `Looper.isPerfLogEnable()`).  

3. **ANR and Termination**  
   - UI thread blockage (`ANR in ModalActivity`) after >10 seconds of unresponsiveness:  
     ```
     ANR in Window{868588b u0 com.instagram.android/com.instagram.modal.ModalActivity}  
     Waited 10002ms for MotionEvent  
     ```  
   - Forced app termination by the OS.

### **Attack Vector**
An attacker can send a message containing a malformed drawable (e.g., via group chat). All clients that render the message experience catastrophic memory exhaustion and crashes.

## **Proof of Concept**
1. Craft a drawable resource with invalid metadata or reference a non-existent resource ID (e.g., `0x7f0802d7`).  
2. Send the malicious drawable to a group chat.  
3. Observe client-side crashes across all devices that load the message.  

*Video Proof*: 

https://github.com/user-attachments/assets/9c92a199-9efd-450c-a01b-51c8d3817576


## **Impact**
- **Availability**: User who view the message either have their system or app crash
- **Scope**: All users in a group chat who view the message.  

## **Remediation**
- **Input Validation**: Validate resource integrity before inflation.  
- **Exception Handling**: Implement graceful failure for `ResourceNotFoundException` (e.g., fallback assets).  
- **Memory Safeguards**: Terminate threads after repeated allocation failures.  

## **References**
- Affected Version: [Google Play Store v370.1.0.43.96](https://play.google.com/store/apps/details?id=com.instagram.android)  and below
- Log Excerpts: Internal crash logs (attached).  

## **Disclosure Timeline**
- **Report Date**: 3/8/25
- **CNA Report Date**: 3/9/25
