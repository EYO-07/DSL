using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using OpenHardwareMonitor;
using OpenHardwareMonitor.Hardware; // Assuming this is the namespace from OpenHardwareLib.dll

namespace MiniSystemMonitor
{
    public class OpenHardwareLibWrapper
    {
        // Vectors (Lists) for each hardware type
        public List<HardwareInfo> CpuInfo { get; private set; }
        public List<HardwareInfo> GpuInfo { get; private set; }
        public List<HardwareInfo> RamInfo { get; private set; }
        public List<HardwareInfo> DiskInfo { get; private set; }

        // Dictionary to map hardware names to HardwareInfo objects
        public Dictionary<string, HardwareInfo> HardwareDict { get; private set; }

        // OpenHardwareMonitor Computer object to access hardware
        private readonly Computer _computer;

        // Constructor
        public OpenHardwareLibWrapper()
        {
            // Initialize collections
            CpuInfo = new List<HardwareInfo>();
            GpuInfo = new List<HardwareInfo>();
            RamInfo = new List<HardwareInfo>();
            DiskInfo = new List<HardwareInfo>();
            HardwareDict = new Dictionary<string, HardwareInfo>();

            // Initialize OpenHardwareMonitor Computer object
            _computer = new Computer
            {
                CPUEnabled = true,
                GPUEnabled = true,
                RAMEnabled = true,
                HDDEnabled = true
            };
            _computer.Open(); // Open the computer for monitoring
        }

        // Update hardware information
        public void UpdateInfo()
        {
            // Clear existing lists to refresh data
            CpuInfo.Clear();
            GpuInfo.Clear();
            RamInfo.Clear();
            DiskInfo.Clear();

            // Iterate through all hardware components
            foreach (IHardware hardware in _computer.Hardware)
            {
                hardware.Update(); // Update sensor data

                // Determine hardware type and process accordingly
                if (hardware.HardwareType == HardwareType.CPU)
                {
                    ProcessHardware(hardware, "CPU", CpuInfo);
                }
                else if (hardware.HardwareType == HardwareType.GpuAti ||
                         hardware.HardwareType == HardwareType.GpuNvidia)
                {
                    ProcessHardware(hardware, "GPU", GpuInfo);
                }
                else if (hardware.HardwareType == HardwareType.RAM)
                {
                    ProcessHardware(hardware, "RAM", RamInfo);
                }
                else if (hardware.HardwareType == HardwareType.HDD)
                {
                    ProcessHardware(hardware, "Disk", DiskInfo);
                }
            }
        }

        // Helper method to process hardware and update collections
        private void ProcessHardware(IHardware hardware, string type, List<HardwareInfo> infoList)
        {
            double load = 0.0;
            double temperature = 0.0;
            double fanRpm = 0.0;

            // Iterate through sensors to extract data
            foreach (ISensor sensor in hardware.Sensors)
            {
                if (sensor.SensorType == SensorType.Load)
                {
                    load = sensor.Value.HasValue ? sensor.Value.Value : 0.0;
                }
                else if (sensor.SensorType == SensorType.Temperature)
                {
                    temperature = sensor.Value.HasValue ? sensor.Value.Value : 0.0;
                }
                else if (sensor.SensorType == SensorType.Fan)
                {
                    fanRpm = sensor.Value.HasValue ? sensor.Value.Value : 0.0;
                }
            }

            // Create or update HardwareInfo object
            string hardwareName = hardware.Name;
            if (HardwareDict.ContainsKey(hardwareName))
            {
                // Update existing entry
                HardwareInfo existingInfo = HardwareDict[hardwareName];
                existingInfo.Load = load;
                existingInfo.Temperature = temperature;
                existingInfo.FanRpm = fanRpm;
            }
            else
            {
                // Create new HardwareInfo and add to dictionary and list
                HardwareInfo newInfo = new HardwareInfo(hardwareName, type, load, temperature, fanRpm);
                HardwareDict[hardwareName] = newInfo;
                infoList.Add(newInfo);
            }
        }

        // Dispose method to clean up resources (optional but recommended)
        public void Dispose()
        {
            _computer.Close();
        }
    }
}