# Mine Coaches

## Usage

To execute the main script run the following command:

```bash
python3 -m mine.main
```

This program has a long runtime as it executes a number of operation
and executes many requests to determine what it needs to. In order
to iterate quickly and dynamicaly figure out what is needed I have
to make it reentrant. This means that it can be paused and resumed
without unnecessarily duplicating work while it is doing what it does.

## Reentrancy

To make your program reentrant, you need to ensure that it can be paused and resumed without losing its current state. Here's a step-by-step guide on how to achieve reentrancy in your program:

1. **Identify Checkpoints**:
   Divide your long-running process into logical checkpoints or stages where you can save the current state. These checkpoints should represent parts of the process that can be paused and resumed without losing progress.

2. **Serialize State**:
   For each checkpoint, serialize the relevant state into a file or database. Serialization involves converting the current state (variables, data, and any other necessary information) into a format that can be saved and later deserialized.

3. **Deserialize State**:
   When resuming the program, read the serialized state from the storage location and deserialize it to restore the program to its previous state.

4. **Handle Dependencies**:
   Ensure that the program can handle any dependencies or changes that may have occurred between checkpoints. For example, if external data sources have changed, the program should account for this and reconcile any differences.

5. **Error Handling and Recovery**:
   Implement proper error handling and recovery mechanisms. If the program is interrupted due to an error or failure, it should be able to resume from a previous checkpoint. Handle exceptions and failures gracefully, and provide recovery options.

6. **Concurrency Considerations**:
   If your program involves concurrent execution, ensure that the reentrant approach is thread-safe and doesn't lead to data corruption. Use appropriate locks or synchronization mechanisms to manage concurrent access to shared resources.

7. **Testing and Validation**:
   Thoroughly test your reentrant program to ensure that it can be reliably paused and resumed without data loss or errors. Test different scenarios, including interruptions due to errors or external events.

8. **Documentation**:
   Document the reentrant functionality in your program, including how to pause and resume it, the supported checkpoints, and any special considerations for users or developers.

By following these steps, you can make your program reentrant, allowing you to pause and resume its execution without losing progress or data. This is especially useful for long-running processes and critical applications where interruptions can occur.

