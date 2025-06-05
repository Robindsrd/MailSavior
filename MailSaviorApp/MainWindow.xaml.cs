using System.Windows;
using System.DirectoryServices.AccountManagement;

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

            bool isDev = true;

            if (isDev)
            {
                if (username == "admin" && password == "admin")
                {
                    var dashboard = new UserDashboard();
                    dashboard.Show();
                    this.Close();
                }
                else
                {
                    ErrorMessage.Text = "Identifiants de test incorrects (admin / admin).";
                    ErrorMessage.Visibility = Visibility.Visible;
                }
            }
            else
            {
                try
                {
                    using (var context = new PrincipalContext(ContextType.Domain, "MAILSAVIOR.LOCAL"))
                    {
                        bool isValid = context.ValidateCredentials(username, password);

                        if (isValid)
                        {
                            var dashboard = new UserDashboard();
                            dashboard.Show();
                            this.Close();
                        }
                        else
                        {
                            ErrorMessage.Text = "Échec de l'authentification LDAP.";
                            ErrorMessage.Visibility = Visibility.Visible;
                        }
                    }
                }
                catch
                {
                    ErrorMessage.Text = "Erreur lors de la connexion à Active Directory.";
                    ErrorMessage.Visibility = Visibility.Visible;
                }
            }
        }

    }
}
