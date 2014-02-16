using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Crawler.Common
{
    class FileIO
    {
        private const string LogPath = "log.txt";
        private static StreamWriter logWriter;

        public static Task WriteFileAsync(string path, byte[] content)
        {
            string dirName = Path.GetDirectoryName(path);
            Directory.CreateDirectory(dirName);
            return Task.Factory.StartNew(() =>
            {
                File.WriteAllBytes(path, content);
            });
        }

        public static void Log(string logMessage)
        {
            if (logWriter == null)
            {
                logWriter = File.AppendText(LogPath);
                logWriter.AutoFlush = true;
            }

            logWriter.WriteLine(logMessage);
        }
    }
}
