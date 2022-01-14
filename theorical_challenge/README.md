# Theorical Challenge

## Processes, Threads and Coroutines

- _One case where you would use processes to solve a problem and why_

    - Processes have some advantages and disadvantages compared with threads according to the resources and how those resources are managed. The kind of problems I would solve with processes are independent tasks that ensure if one process fail doesn't affect any other processes. For example scraping programs that fetch data from different competitors web pages, if one program fails it doesn't interferes with the fetching task of the other processes.

- _One case where you would use threads to solve a problem and why_
   
   -  Threads are really useful to accomplish tasks concurrently, however it's not so efficient to conmunicate between each other so a thread solution fits for specific tasks. One case would be the call to an API several times, it doesn't include any processing of the response. On this kind of cases it's necessary to have in mind that every time one task finished then the thread die and for the next concurrent call the process need to create a new thread.

- _One case where you would use coroutines to solve a problem and why_
   
   - Coroutines have several advantages because it's more efficient than threads since it auto-manages their switching to assing resources, the communication between each other is easy, between others. One very interesting property is that one coroutine can be re-used several times without the need to create more. One case where the coroutine is useful is with processes than have several tasks to be done, taking the above example one coroutine can be in charge of the calls to the API, another coroutine can receive the data and clean it and after all can exist a last coroutine that is in charge of saving the data to some database. I you note the difference this case implies a process with more tasks that conmunicate between them.

## Optimization of operating system resources

- _If you have 1.000.000 of elements and you have to check information for each of them in an API HTTP. ¿How you would do it? Explain_

    - For this problem the better solution will be accomplished using coroutines. Since the problem is a very specific task and threads are a possibility, we have to remember that is expensive on resourses to create a new thread after a call to the API is done and that is a problem that we don't have with coroutines. The key strategy is to create a pool of coroutines, big enough that the computer and network supports, that will be calling the API HTTP concurrently until accomplish the 1.000.000 calls.

