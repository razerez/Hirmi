using System;
using System.Collections.Generic;
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
using System.Diagnostics;
using System.IO;

namespace wpfBasics
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
		
        public MainWindow()
        {
            InitializeComponent();
        }

		private void Record_Click(object sender, RoutedEventArgs e)
		{
			ProcessStartInfo pythonInfo = new ProcessStartInfo();
			Process python;
			pythonInfo.FileName = "C:\\Python36\\python.exe";
			pythonInfo.Arguments = "C:\\Users\\user\\repos\\beer_sheva-202-hirmi\\Hirmi\\Hirmi.py";
			pythonInfo.CreateNoWindow = false;
			pythonInfo.UseShellExecute = true;

			Console.WriteLine("Python Starting");
			python = Process.Start(pythonInfo);
			python.WaitForExit();
			python.Close();

		}
		
	}
}
