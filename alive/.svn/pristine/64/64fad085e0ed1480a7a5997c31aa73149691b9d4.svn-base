using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SQLite;

namespace Crawler.Database.Table
{
    class HtmlPage : TableBase
    {
        [MaxLength(256), Unique]
        public string Uri { get; set; }
        public byte[] Content { get; set; }
        public int? PostId { get; set; }
    }
}
