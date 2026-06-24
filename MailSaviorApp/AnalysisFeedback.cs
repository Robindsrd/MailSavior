namespace MailSaviorApp
{
    /// <summary>
    /// Retour utilisateur envoyé à l'API. Volontairement minimisé :
    /// on n'envoie jamais le corps de l'e-mail, seulement sa longueur.
    /// </summary>
    public class AnalysisFeedback
    {
        public double suspicion_score { get; set; }
        public string feedback { get; set; }
        public string predicted_label { get; set; }
        public int text_length { get; set; }
    }
}
