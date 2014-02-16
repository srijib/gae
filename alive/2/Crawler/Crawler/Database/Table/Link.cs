using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SQLite;

namespace Crawler.Database.Table
{
    public enum LinkStatus
    {
        Pending,
        Processing,
        Success,
    }

    public enum LinkType
    {
        Unknown,
        Page,
        Image,
    }

    class Link : TableBase
    {
        [MaxLength(256), Unique]
        public string Uri { get; set; }
        public LinkType Type { get; set; }
        public LinkStatus Status { get; set; }
        public int? PostId { get; set; }
    }
}
