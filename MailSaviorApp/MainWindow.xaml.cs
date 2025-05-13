using System.Windows;

namespace MailSaviorApp
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void LoginButton_Click(object sender, RoutedEventArgs e)
        {
            string username = UsernameBox.Text;
            string password = PasswordBox.Password;

            
            if (username == "admin" && password == "admin")
            {
                ErrorMessage.Visibility = Visibility.Collapsed;

                UserDashboard dashboard = new UserDashboard();
                dashboard.Show();

                
                this.Close();
            }
            else
            {
                ErrorMessage.Visibility = Visibility.Visible;
            }
        }

    }
}
