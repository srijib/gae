using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Crawler.Common;
using Crawler.Database;
using Crawler.Database.Table;
using C = Crawler.Model.Crawler;

namespace Crawler
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window, IDisposable
    {
        private static TextBox LogTextBox = null;

        private const string StartUrl = "http://www.mnsfz.com/";
        C crawler = new C(StartUrl);
        //private readonly object sync = new object();

        public MainWindow()
        {
            InitializeComponent();
            LogTextBox = this.LogBox;
        }

        public static void LogWriteLine(string text)
        {
            if (LogTextBox != null)
            {
                LogTextBox.Text += string.Format(CultureInfo.InvariantCulture, "{0}{1}", text, Environment.NewLine);
            }
        }

        public void Dispose()
        {
            this.Dispose(true);
            GC.SuppressFinalize(this);
        }

        ~MainWindow()
        {
            this.Dispose(false);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (disposing)
            {
                this.crawler.Dispose();
            }

            // no native resources
        }

        private async void TestButtonClick(object sender, RoutedEventArgs e)
        {
            this.TestButton.IsEnabled = false;
            await this.crawler.StartOrContinue();
            this.TaskTestButton.IsEnabled = true;
        }

        private void TestTaskButtonClick(object sender, RoutedEventArgs e)
        {
            this.TaskTestButton.IsEnabled = false;
            this.crawler.NotifyWorkersStop();
            this.TestButton.IsEnabled = true;
        }

        //private void TestQueueSpeed()
        //{
        //    ThreadSafeUniqueQueue<string> q = new ThreadSafeUniqueQueue<string>();
        //    q.Enqueue("test");
        //    q.Dequeue();
        //}

        //private void TestQueueSync()
        //{
        //    ThreadSafeUniqueQueue<string> q = new ThreadSafeUniqueQueue<string>();
        //    for (int i = 0; i < 20; i++)
        //    {
        //        q.Enqueue(i.ToString(CultureInfo.InvariantCulture));
        //    }

        //    for (int i = 0; i < 21; i++)
        //    {
        //        Task.Factory.StartNew(this.RunDequeue, q);
        //    }
        //}

        //private void RunDequeue(object queue)
        //{

        //    ThreadSafeUniqueQueue<string> q = queue as ThreadSafeUniqueQueue<string>;
        //    lock (this.sync)
        //    {
        //        string ii = q.Dequeue();
        //        System.Diagnostics.Debug.Write("D" + ii + ", ");
        //    }
        //}

        //private void RunQueueTask(object i)
        //{
        //    string integer;
        //    integer = i.ToString();
        //    lock (this.sync)
        //    {
        //        q.Enqueue(integer);
        //        System.Diagnostics.Debug.Write("E" + integer + ", ");
        //    }
        //    lock (this.sync)
        //    {
        //        integer = q.Dequeue();
        //        System.Diagnostics.Debug.Write("D" + integer + ", ");
        //    }
        //}
    }
}
