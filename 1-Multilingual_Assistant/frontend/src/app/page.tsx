"use client";

import { useState, useEffect, useRef } from "react";
import { translateText, sendChat } from "@/lib/api";

// Hook: reveal element on scroll into view
function useRevealOnScroll() {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return { ref, isVisible };
}

interface Message {
  type: "user" | "bot";
  text: string;
}

const FAQ_CHIPS = [
  "How to order?",
  "Payment methods?",
  "Track order?",
  "Return policy?",
  "Contact support?",
];

const LANGUAGES = [
  { code: "auto", name: "Auto Detect" },
  { code: "en", name: "English" },
  { code: "es", name: "Spanish" },
  { code: "fr", name: "French" },
  { code: "de", name: "German" },
  { code: "ur", name: "Urdu" },
  { code: "hi", name: "Hindi" },
];

export default function Home() {
  // Reveal refs for scroll-triggered animations
  const heroRef = useRevealOnScroll();
  const statsRef = useRevealOnScroll();
  const featuresRef = useRevealOnScroll();
  const translatorRef = useRevealOnScroll();
  const faqRef = useRevealOnScroll();

  // Translation state
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [sourceLang, setSourceLang] = useState("auto");
  const [targetLang, setTargetLang] = useState("ur");
  const [translateStatus, setTranslateStatus] = useState("");
  const [isTranslating, setIsTranslating] = useState(false);

  // Chatbot state
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatStatus, setChatStatus] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showTyping, setShowTyping] = useState(false);
  const chatWindowRef = useRef<HTMLDivElement>(null);

  // Add welcome message on mount
  useEffect(() => {
    setMessages([
      {
        type: "bot",
        text: "👋 Hi! Ask me anything.",
      },
    ]);
  }, []);

  // Scroll chat to bottom
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages, showTyping]);

  const handleTranslate = async () => {
    if (!inputText.trim()) {
      setTranslateStatus("Please enter text to translate.");
      return;
    }

    setIsTranslating(true);
    setTranslateStatus("Translating...");

    try {
      const result = await translateText({
        text: inputText,
        source_lang: sourceLang,
        target_lang: targetLang,
      });
      setOutputText(result.translated_text);
      setTranslateStatus("Done!");
    } catch (error) {
      console.error(error);
      setTranslateStatus("Failed. Try again.");
    } finally {
      setIsTranslating(false);
    }
  };

  const handleSwapLanguages = () => {
    const tempLang = sourceLang;
    setSourceLang(targetLang);
    setTargetLang(tempLang);

    const tempText = inputText;
    setInputText(outputText);
    setOutputText(tempText);
  };

  const handleCopy = async () => {
    if (!outputText) return;
    try {
      await navigator.clipboard.writeText(outputText);
      setTranslateStatus("Copied!");
      setTimeout(() => setTranslateStatus("Translation completed successfully."), 1500);
    } catch {
      setOutputText("");
      setOutputText(outputText);
    }
  };

  const handleSendChat = async () => {
    if (!chatInput.trim()) return;

    const userMsg = chatInput.trim();
    setChatInput("");
    setMessages((prev) => [...prev, { type: "user", text: userMsg }]);
    setChatStatus("Thinking...");
    setShowTyping(true);

    try {
      const result = await sendChat(userMsg);
      setMessages((prev) => [...prev, { type: "bot", text: result.answer }]);
      setChatStatus("Ready");
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "Sorry, something went wrong." },
      ]);
      setChatStatus("Error");
    } finally {
      setShowTyping(false);
    }
  };

  const handleChipClick = (chip: string) => {
    setChatInput(chip);
  };

  return (
    <>
      {/* Aurora Background */}
      <div className="aurora aurora-1" />
      <div className="aurora aurora-2" />
      <div className="aurora aurora-3" />

      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-circle">🌐</div>
            <div>
              <h1>AI Language Assistant</h1>
              <p>Translate. Understand. Communicate.</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="container">
        {/* Hero */}
        <section ref={heroRef.ref} className={`hero ${heroRef.isVisible ? "visible reveal" : "reveal"}`}>
          <div className="hero-content">
            <span className="hero-badge">🚀 AI Powered Language Intelligence</span>
            <h2 className="hero-title">Break Language Barriers with Smart AI</h2>
            <p className="hero-subtitle">
              Instantly translate text across multiple languages and interact with an
              intelligent semantic FAQ assistant that understands meaning—not just
              keywords.
            </p>
            <div className="hero-actions">
              <a href="#translator" className="hero-btn">Start Translating</a>
              <a href="#faq" className="hero-btn-outline">Explore Chatbot</a>
            </div>
          </div>
        </section>

        {/* Stats */}
        <section ref={statsRef.ref} className={`stats-grid ${statsRef.isVisible ? "visible reveal" : "reveal"}`}>
          <div className="stat-card">
            <h3>6+</h3>
            <p>Supported Languages</p>
          </div>
          <div className="stat-card">
            <h3>24/7</h3>
            <p>AI Assistance</p>
          </div>
          <div className="stat-card">
            <h3>⚡</h3>
            <p>Fast Responses</p>
          </div>
          <div className="stat-card">
            <h3>🧠</h3>
            <p>Semantic Understanding</p>
          </div>
        </section>

        {/* Features */}
        <section ref={featuresRef.ref} className={`features ${featuresRef.isVisible ? "visible reveal" : "reveal"}`}>
          <div className="feature-card">
            <div className="feature-icon">🌍</div>
            <h3>Smart Translation</h3>
            <p>
              Translate text instantly using AI-powered language processing and multilingual
              support.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🧠</div>
            <h3>Semantic FAQ</h3>
            <p>
              Understands user intent and context rather than matching exact words.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Real-Time Results</h3>
            <p>
              Fast, responsive interactions designed for productivity and support workflows.
            </p>
          </div>
        </section>

        {/* Main Grid */}
        <section className="app-grid">
          {/* Translator */}
          <section ref={translatorRef.ref} id="translator" className={`card ${translatorRef.isVisible ? "visible reveal" : "reveal"}`}>
            <div className="section-header">
              <div>
                <h2>🌐 Translation</h2>
              </div>
            </div>

            <div className="row">
              <label>Source Language</label>
              <select
                value={sourceLang}
                onChange={(e) => setSourceLang(e.target.value)}
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="swap-container">
              <button
                type="button"
                onClick={handleSwapLanguages}
                className="swap-btn"
              >
                ⇄ Swap Languages
              </button>
            </div>

            <div className="row">
              <label>Target Language</label>
              <select
                value={targetLang}
                onChange={(e) => setTargetLang(e.target.value)}
              >
                {LANGUAGES.filter(l => l.code !== "auto").map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="row">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                rows={6}
                placeholder="Type or paste text here..."
              />
            </div>

            <div className="actions">
              <button
                onClick={handleTranslate}
                disabled={isTranslating}
                className="btn"
              >
                {isTranslating ? "⏳ Translating..." : "Translate"}
              </button>
              <button
                onClick={handleCopy}
                disabled={!outputText}
                className="btn btn-secondary"
              >
                Copy Result
              </button>
            </div>

            <div className="row">
              <textarea
                value={outputText}
                rows={6}
                placeholder="Translation appears here..."
                readOnly
              />
            </div>

            <div className="hint">{translateStatus}</div>
          </section>

          {/* Chatbot */}
          <section ref={faqRef.ref} id="faq" className={`card ${faqRef.isVisible ? "visible reveal" : "reveal"}`}>
            <div className="section-header">
              <div>
                <h2>🤖 FAQ Assistant</h2>
              </div>
            </div>

            <div className="faq-intro">
              <div className="faq-chips">
                {FAQ_CHIPS.map((chip) => (
                  <button
                    key={chip}
                    onClick={() => handleChipClick(chip)}
                    className="faq-chip"
                  >
                    {chip}
                  </button>
                ))}
              </div>
            </div>

            <div ref={chatWindowRef} className="chat-window">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`bubble ${msg.type === "user" ? "bubble-user" : "bubble-bot"}`}
                >
                  <div className="bubble-meta">
                    {msg.type === "user" ? "You" : "AI Assistant"}
                  </div>
                  <div>{msg.text}</div>
                </div>
              ))}
              {showTyping && (
                <div className="bubble bubble-bot">
                  <div className="bubble-meta">AI Assistant</div>
                  <div>⏳ Thinking...</div>
                </div>
              )}
            </div>

            <div className="chat-input">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSendChat()}
                placeholder="Ask your question..."
              />
              <button
                onClick={handleSendChat}
                disabled={isLoading}
                className="btn"
              >
                Send
              </button>
            </div>

            <div className="hint">{chatStatus}</div>
          </section>
        </section>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>Built with AI • Semantic Search • Multilingual Intelligence</p>
      </footer>
    </>
  );
}