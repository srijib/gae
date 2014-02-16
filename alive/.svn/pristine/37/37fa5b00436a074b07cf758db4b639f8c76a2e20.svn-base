using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Controls;

namespace Crawler.Common
{
    class Utils
    {
        public static async Task LogAsync(string text)
        {
            int threadId = Thread.CurrentThread.ManagedThreadId;
            // Debug.Listeners.Add(new TextWriterTraceListener(Console.Out));
            await UIRunAsync(() =>
            {
                DebugWriteLine(threadId, text);
            });
        }

        public static void LogSync(string text)
        {
            int threadId = Thread.CurrentThread.ManagedThreadId;
            UIRunSync(() =>
            {
                DebugWriteLine(threadId, text);
            });
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Globalization", "CA1303:请不要将文本作为本地化参数传递", MessageId = "Crawler.MainWindow.LogWriteLine(System.String)")]
        private static void DebugWriteLine(int threadId, string text)
        {
            string line = string.Format(CultureInfo.InvariantCulture, "Thread({0}): {1}", threadId, text);
            MainWindow.LogWriteLine(line);
            Debug.WriteLine(line);
            FileIO.Log(line);
        }

        public static async Task UIRunAsync(Action action)
        {
            await App.Current.Dispatcher.InvokeAsync(action);
        }

        public static void UIRunSync(Action action)
        {
            App.Current.Dispatcher.Invoke(action);
        }
    }
}
