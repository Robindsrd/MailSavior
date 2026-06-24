using System;

namespace MailSaviorApp
{
    /// <summary>
    /// Configuration centralisée de l'API IA (évite les URL en dur dispersées).
    /// Surchargée par la variable d'environnement MAILSAVIOR_API_URL si présente.
    /// </summary>
    public static class ApiConfig
    {
        public static string BaseUrl =>
            Environment.GetEnvironmentVariable("MAILSAVIOR_API_URL") ?? "http://127.0.0.1:8000";

        public static readonly TimeSpan Timeout = TimeSpan.FromSeconds(10);
    }
}
