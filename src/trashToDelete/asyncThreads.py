'''
async def __async_init(self, thread_id: int):
    # Если что-то сломалось, то именно это будет перезапускать бесконечно
    async with aiohttp.ClientSession() as session:
        tasks = []

        while not self.q.empty() and len(tasks) < self.MAX_TASKS:
            title: Title = self.q.get()
            task = asyncio.create_task(self.__worker(session, title))
            tasks.append(task)

        print(f'{len(tasks)} tasks created for {thread_id} thread')

        if len(tasks) == 0:
            return 0

        try:
            await asyncio.gather(*tasks)
        except Exception:
            for task in tasks:
                task.cancel()

def __thread_init(self, thread_id: int):
    asyncio.set_event_loop(asyncio.new_event_loop())

    while True:
        tasks_count = asyncio.run(self.__async_init(thread_id))

        if tasks_count == 0:
            break




threads = [threading.Thread(target=self.__thread_init, args=(j,)) for j in range(threads_count)]

for thread in threads:
    thread.start()

for task in threads:
    task.join()
'''