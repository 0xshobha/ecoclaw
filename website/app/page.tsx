import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import ProblemSolution from "./components/ProblemSolution";
import HowItWorks from "./components/HowItWorks";
import LiveDemo from "./components/LiveDemo";
import SponsorIntegrations from "./components/SponsorIntegrations";
import Features from "./components/Features";
import Impact from "./components/Impact";
import Footer from "./components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-navy overflow-x-hidden">
      <Navbar />
      <Hero />
      <ProblemSolution />
      <HowItWorks />
      <SponsorIntegrations />
      <Features />
      <LiveDemo />
      <Impact />
      <Footer />
    </main>
  );
}
