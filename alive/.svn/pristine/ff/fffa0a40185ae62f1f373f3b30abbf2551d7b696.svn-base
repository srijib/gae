using System;
using System.Collections;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Crawler.Common
{
    public class ThreadSafeUniqueQueue<T> : Queue<T>, IDisposable
    {
        private readonly ConcurrentQueue<T> internalQueue = new ConcurrentQueue<T>();
        private readonly BlockingCollection<T> blockingCollection;
        private readonly HashSet<T> set = new HashSet<T>();
        private readonly object sync = new object();

        public ThreadSafeUniqueQueue()
        {
            this.blockingCollection = new BlockingCollection<T>(this.internalQueue);
        }

        public new T Dequeue()
        {
            lock (this.sync)
            {
                T item = this.blockingCollection.Take();
                this.set.Remove(item);
                return item;
            }
        }

        public new bool Enqueue(T item)
        {
            lock (this.sync)
            {
                if (this.set.Add(item))
                {
                    this.blockingCollection.Add(item);
                    return true;
                }
                else
                {
                    // already existed
                    return false;
                }
            }
        }

        public void Dispose()
        {
            this.Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (disposing)
            {
            }

            // no native resources
        }
    }
}
