using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MiniSystemMonitor
{
    public class HardwareInfo
    {
        // Properties as per the declarative description
        public string Name { get; set; }
        public string Type { get; set; }
        public double Load { get; set; }
        public double Temperature { get; set; }
        public double FanRpm { get; set; }

        // Constructor to initialize the properties
        public HardwareInfo(string name, string type, double load, double temperature, double fanRpm)
        {
            Name = name;
            Type = type;
            Load = load;
            Temperature = temperature;
            FanRpm = fanRpm;
        }

        // Method to return formatted string: initial of name + ": " + load% + temperature°C + fan RPM
        public string Info()
        {
            // Get the first character of the name (initial)
            string initial = string.IsNullOrEmpty(Name) ? "" : Name.Substring(0, 1);
            // Format the string as specified
            return $"{initial}: {Load:F1}% {Temperature:F1}°C {FanRpm:F0} RPM";
        }
    }
}