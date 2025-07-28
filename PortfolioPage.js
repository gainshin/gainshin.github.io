import React from 'react';
import { Mail, Linkedin, ArrowRight, BrainCircuit, ShieldCheck, Briefcase, FileText, Youtube, AppWindow, Play, ChevronDown, ChevronUp } from 'lucide-react';

const professionalExperience = [
    {
        period: '2023 - Present',
        role: 'AI/UX Consultant',
        company: 'Privacyux consulting ltd',
        location: 'Montreal, Canada',
        description: [
            'Pioneered Agentic UX framework implementation for 15+ AI startups and academic labs, resulting in a 40% improvement in user trust metrics.',
            'Developed Privacy-as-Trust design strategy helping clients integrate PIPEDA and GDPR compliance into product core architecture.',
            'Architected human-centered AI systems focusing on Social Agents, Voice Interaction, and private Generative AI solutions.',
        ],
    },
    {
        period: '2023 - 2024',
        role: 'AI/UX Strategy Architect',
        company: 'Bondee',
        location: 'Singapore',
        description: [
            'Successfully launched 5 innovative AI-driven products in 2024, including K12 Educational Voice Companion and Enterprise-Level Gen-AI assets Library.',
            'Spearheaded internal AI governance and compliance reviews for high-risk AI systems, reducing legal liability exposure by 60%.',
        ],
    },
    {
        period: '2021 - 2023',
        role: 'Special consultant to CEO',
        company: 'Cyphant group',
        location: 'Beijing, San Francisco Bay Area',
        description: [
            'Led design and implementation of user-centric Generative AI/LLM solutions in production environments for enterprise clients.',
            'Orchestrated data-driven design methodologies for contextual AI interactions.',
            'Championed UX best practices across engineering teams, establishing user-first design culture.',
        ],
    },
    {
        period: '2017 - 2018',
        role: 'User Experience Architect',
        company: 'Alibaba.com',
        location: 'Hangzhou, China',
        description: [
            'Founded Alibaba Design University, a comprehensive design education program for 500+ designers.',
            'Pioneered "Alimama AI-Copywriter" - a groundbreaking ML-powered content generation tool processing 100+ million copy samples.',
        ],
    },
];

const products = [
    {
        title: "AIPET Studio Platform",
        description: "A learning platform for Figma Design Tokens and AIPET framework practice, built for designers.",
        url: "https://app--aipet-studio-ddc44a58.base44.app/Dashboard",
        image: "https://qtrypzzcjebvfcihiynt.supabase.co/storage/v1/object/public/base44-prod/public/ecc1cfcd1_Screenshot2025-07-28at122139.png"
    },
    {
        title: "Token Analyzer",
        description: "Automatically analyze Figma exports or code to extract and create Design Tokens, bridging design and development.",
        url: "https://app--aipet-studio-ddc44a58.base44.app/Dashboard",
        image: "https://qtrypzzcjebvfcihiynt.supabase.co/storage/v1/object/public/base44-prod/public/302099382_Screenshot2025-07-28at122913.png"
    },
    {
        title: "Research Tracking Matrix",
        description: "Automatically generates tracking points based on your research scope across six key areas: Priority, Theory, Tech, Industry, Academia, and Key Opinion Leaders.",
        url: "https://app--aiux-pulse-709cc847.base44.app/",
        image: "https://qtrypzzcjebvfcihiynt.supabase.co/storage/v1/object/public/base44-prod/public/aad130959_Screenshot2025-07-28at123326.png"
    }
];

const writings = [
    {
        title: "Traditional Design Systems",
        description: "Exploring the evolution from static rulebooks to intelligent 'Experience Systems' powered by AI.",
        url: "https://www.linkedin.com/pulse/your-design-system-asset-liability-evaluating-agentic-joshua-hsiao-jaxuc/?trackingId=wOTY4DxZ86yUkBl2ek5FNg%3D%3D",
        image: "https://qtrypzzcjebvfcihiynt.supabase.co/storage/v1/object/public/base44-prod/public/63641fd8a_Screenshot2025-07-28at122002.png"
    },
    {
        title: "AIPET: Agency",
        description: "A framework for AI Product Managers to navigate the dilemma between autonomous agents and helpful copilots.",
        url: "https://www.linkedin.com/pulse/your-design-system-asset-liability-evaluating-agentic-joshua-hsiao-wlycc/?trackingId=kZfoySUFxd%2F2cTyqQyQ%2FFw%3D%3D",
        image: "https://qtrypzzcjebvfcihiynt.supabase.co/storage/v1/object/public/base44-prod/public/a603415e2_Screenshot2025-07-28at122021.png"
    },
    {
        title: "Design Principles x Token",
        description: "How the AIPET framework translates into machine-readable instructions through Design Tokens.",
        url: "https://www.linkedin.com/pulse/designing-ai-companions-minors-ux-framework-proactive-joshua-hsiao-jj7nf/?trackingId=v6kAz1LrRaexQiLRAeI7mQ%3D%3D",
        image: "https://qtrypzzcjebvfcihiynt.supabase.co/storage/v1/object/public/base44-prod/public/e562d6509_Screenshot2025-07-28at122038.png"
    }
];

const youtubeVideos = [
    {
        title: "Agentic UX Series - Part I",
        description: "Is Your Design System an Asset or a Liability? Evaluating Agentic Experiences with the AIPET Framework",
        url: "https://www.youtube.com/watch?v=b6Qb-w9DT60",
        image: "https://qtrypzzcjebvfcihiynt.supabase.co/storage/v1/object/public/base44-prod/public/6608e0eb0_Screenshot2025-07-27at165130.png"
    },
    {
        title: "Agentic UX Series - Part II",
        description: "Answering the Skeptics: Why We Need an \"Experience System,\" Not Just an \"Adaptive\" One. Evaluating Agentic Experiences with the AIPET Framework",
        url: "https://www.youtube.com/watch?v=CMyU0GI94NI",
        image: "https://qtrypzzcjebvfcihiynt.supabase.co/storage/v1/object/public/base44-prod/public/4568b0cde_Screenshot2025-07-27at185302.png"
    }
];

const skills = {
    "AI & Agentic UX": ["AI agent workflow", "Agentic UX", "Human-Centered AI", "AI Trend Analysis & Foresight"],
    "Privacy & Ethics": ["Privacy-first Design", "AI Ethics & Governance", "GDPR & PIPEDA Compliance", "Data Governance Strategy"],
    "Design & Strategy": ["UX/Design Leadership", "AI Product Strategy & Roadmapping", "Service Design Strategy", "Startup Consulting & Mentoring"]
};


export default function PortfolioPage() {
    const [showAllExperience, setShowAllExperience] = React.useState(false);

    // Split experience into recent (2023-2025) and older
    const recentExperience = professionalExperience.slice(0, 2);
    const olderExperience = professionalExperience.slice(2);

    return (
        <div className="bg-slate-50 min-h-screen">
            <header className="bg-slate-50/80 backdrop-blur-lg sticky top-0 z-50 border-b border-slate-200">
                <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
                    <a href="#" className="text-xl font-bold text-slate-900">Joshua Hsiao</a>
                    <div className="hidden md:flex items-center space-x-6">
                        <a href="#articles" className="text-slate-600 hover:text-teal">Articles</a>
                        <a href="#videos" className="text-slate-600 hover:text-teal">Videos</a>
                        <a href="#experience" className="text-slate-600 hover:text-teal">Experience</a>
                        <a href="#products" className="text-slate-600 hover:text-teal">Products</a>
                        <a href="#skills" className="text-slate-600 hover:text-teal">Skills</a>
                        <a href="#contact" className="bg-teal text-white px-4 py-2 rounded-md hover:bg-teal-dark transition-colors">Contact</a>
                    </div>
                </nav>
            </header>

            <main className="container mx-auto px-6 py-16 md:py-24">
                {/* Hero Section */}
                <section id="hero" className="text-center">
                    <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900">Joshua Hsiao</h1>
                    <h2 className="text-2xl md:text-3xl font-semibold text-teal mt-4">AI/UX CONSULTANT</h2>
                    <p className="max-w-3xl mx-auto mt-8 text-lg text-slate-600">
                        Pioneering Agentic UX for the healthcare and aging sectors. I design proactive, trustworthy AI companions that foster independence, dignity, and connection, placing user privacy and control at the forefront.
                    </p>
                    <div className="mt-8 flex justify-center items-center space-x-4">
                        <a href="mailto:gainshin.hsiao@mail.mcgill.ca" className="inline-flex items-center justify-center p-3 border border-transparent rounded-full text-slate-600 bg-slate-200 hover:bg-slate-300 transition-colors">
                            <Mail className="w-6 h-6" />
                        </a>
                        <a href="https://www.linkedin.com/in/joshuahsiao" target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center p-3 border border-transparent rounded-full text-slate-600 bg-slate-200 hover:bg-slate-300 transition-colors">
                            <Linkedin className="w-6 h-6" />
                        </a>
                        <a href="https://www.youtube.com/@PrivacyUX" target="_blank" rel="noopener noreferrer" className="inline-flex items-center justify-center p-3 border border-transparent rounded-full text-slate-600 bg-slate-200 hover:bg-slate-300 transition-colors">
                            <Youtube className="w-6 h-6" />
                        </a>
                    </div>
                </section>

                {/* Recent Articles Section */}
                <section id="articles" className="mt-24 md:mt-32">
                    <h3 className="text-3xl font-bold text-slate-900 text-center mb-12 flex items-center justify-center gap-3"><FileText className="w-8 h-8 text-teal" />Recent Articles</h3>
                    <div className="grid md:grid-cols-3 gap-8">
                        {writings.map((writing, index) => (
                            <a key={index} href={writing.url} target="_blank" rel="noopener noreferrer" className="block group bg-white rounded-lg border border-slate-200 shadow-sm hover:shadow-lg transition-all overflow-hidden hover:-translate-y-1.5 transform-gpu duration-300">
                                <img src={writing.image} alt={writing.title} className="w-full h-48 object-cover" />
                                <div className="p-6">
                                    <h4 className="text-xl font-bold text-slate-800 group-hover:text-teal transition-colors">{writing.title}</h4>
                                    <p className="mt-2 text-slate-600 text-sm h-16">{writing.description}</p>
                                    <div className="mt-4 flex items-center text-teal font-semibold">
                                        Read More
                                        <ArrowRight className="w-4 h-4 ml-2 transform-gpu transition-transform group-hover:translate-x-1" />
                                    </div>
                                </div>
                            </a>
                        ))}
                    </div>
                    <div className="text-center mt-12">
                        <a
                            href="https://privacyux.substack.com/s/ai-literacy-and-privacy-experience"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-teal text-white px-8 py-3 rounded-md font-semibold hover:bg-teal-dark transition-colors inline-block"
                        >
                            See More Articles
                        </a>
                    </div>
                </section>

                {/* YouTube Videos Section */}
                <section id="videos" className="mt-24 md:mt-32">
                    <h3 className="text-3xl font-bold text-slate-900 text-center mb-12 flex items-center justify-center gap-3"><Youtube className="w-8 h-8 text-teal" />YouTube Channel</h3>
                    <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
                        {youtubeVideos.map((video, index) => (
                            <a key={index} href={video.url} target="_blank" rel="noopener noreferrer" className="block group bg-white rounded-lg border border-slate-200 shadow-sm hover:shadow-lg transition-all overflow-hidden hover:-translate-y-1.5 transform-gpu duration-300 relative">
                                <div className="relative">
                                    <img src={video.image} alt={video.title} className="w-full h-64 object-cover" />
                                    <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                                        <div className="bg-white bg-opacity-90 rounded-full p-4">
                                            <Play className="w-8 h-8 text-teal ml-1" />
                                        </div>
                                    </div>
                                </div>
                                <div className="p-6">
                                    <h4 className="text-xl font-bold text-slate-800 group-hover:text-teal transition-colors">{video.title}</h4>
                                    <p className="mt-2 text-slate-600 text-sm">{video.description}</p>
                                    <div className="mt-4 flex items-center text-teal font-semibold">
                                        Watch Video
                                        <ArrowRight className="w-4 h-4 ml-2 transform-gpu transition-transform group-hover:translate-x-1" />
                                    </div>
                                </div>
                            </a>
                        ))}
                    </div>
                </section>

                {/* Professional Experience */}
                <section id="experience" className="mt-24 md:mt-32">
                    <h3 className="text-3xl font-bold text-slate-900 text-center flex items-center justify-center gap-3"><Briefcase className="w-8 h-8 text-teal" />Professional Experience</h3>
                    <div className="mt-12 relative border-l-2 border-slate-200 ml-6 md:ml-0">

                        {/* Recent Experience (2023-2025) - Always visible */}
                        {recentExperience.map((exp, index) => (
                            <div key={index} className="mb-12 md:pl-12 pl-8">
                                <span className="absolute -left-[11px] top-1 flex items-center justify-center w-6 h-6 bg-teal rounded-full ring-8 ring-slate-50">
                                    <span className="w-2.5 h-2.5 bg-white rounded-full"></span>
                                </span>
                                <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm hover:shadow-lg transition-shadow">
                                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-2">
                                        <h4 className="text-xl font-bold text-slate-900">{exp.role}</h4>
                                        <p className="text-sm text-slate-500 bg-slate-100 px-3 py-1 rounded-full mt-2 md:mt-0">{exp.period}</p>
                                    </div>
                                    <p className="font-semibold text-teal mb-4">{exp.company} &middot; {exp.location}</p>
                                    <ul className="space-y-2 list-disc list-inside text-slate-600">
                                        {exp.description.map((desc, i) => <li key={i}>{desc}</li>)}
                                    </ul>
                                </div>
                            </div>
                        ))}

                        {/* Expand/Collapse Button */}
                        <div className="mb-8 md:pl-12 pl-8">
                            <button
                                onClick={() => setShowAllExperience(!showAllExperience)}
                                className="flex items-center justify-center w-full py-3 px-4 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-200 transition-colors text-slate-600 hover:text-slate-800"
                            >
                                <span className="mr-2">
                                    {showAllExperience ? 'Show Less Experience' : 'Show Earlier Experience'}
                                </span>
                                {showAllExperience ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                            </button>
                        </div>

                        {/* Older Experience - Collapsible */}
                        {showAllExperience && olderExperience.map((exp, index) => (
                            <div key={index + recentExperience.length} className="mb-12 md:pl-12 pl-8">
                                <span className="absolute -left-[11px] top-1 flex items-center justify-center w-6 h-6 bg-slate-400 rounded-full ring-8 ring-slate-50">
                                    <span className="w-2.5 h-2.5 bg-white rounded-full"></span>
                                </span>
                                <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm hover:shadow-lg transition-shadow opacity-90">
                                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-2">
                                        <h4 className="text-xl font-bold text-slate-900">{exp.role}</h4>
                                        <p className="text-sm text-slate-500 bg-slate-100 px-3 py-1 rounded-full mt-2 md:mt-0">{exp.period}</p>
                                    </div>
                                    <p className="font-semibold text-slate-600 mb-4">{exp.company} &middot; {exp.location}</p>
                                    <ul className="space-y-2 list-disc list-inside text-slate-600">
                                        {exp.description.map((desc, i) => <li key={i}>{desc}</li>)}
                                    </ul>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Product Demos */}
                <section id="products" className="mt-24 md:mt-32">
                    <h3 className="text-3xl font-bold text-slate-900 text-center mb-12 flex items-center justify-center gap-3"><AppWindow className="w-8 h-8 text-teal" />Product Demos</h3>
                    <div className="grid md:grid-cols-3 gap-8">
                        {products.map((product, index) => (
                            <a key={index} href={product.url} target="_blank" rel="noopener noreferrer" className="block group bg-white rounded-lg border border-slate-200 shadow-sm hover:shadow-lg transition-all overflow-hidden hover:-translate-y-1.5 transform-gpu duration-300">
                                <img src={product.image} alt={product.title} className="w-full h-48 object-cover object-top" />
                                <div className="p-6">
                                    <h4 className="text-xl font-bold text-slate-800 group-hover:text-teal transition-colors">{product.title}</h4>
                                    <p className="mt-2 text-slate-600 text-sm h-16">{product.description}</p>
                                    <div className="mt-4 flex items-center text-teal font-semibold">
                                        View Demo
                                        <ArrowRight className="w-4 h-4 ml-2 transform-gpu transition-transform group-hover:translate-x-1" />
                                    </div>
                                </div>
                            </a>
                        ))}
                    </div>
                </section>

                {/* Skills Section */}
                <section id="skills" className="mt-24 md:mt-32">
                    <h3 className="text-3xl font-bold text-slate-900 text-center mb-12 flex items-center justify-center gap-3"><BrainCircuit className="w-8 h-8 text-teal" />Core Competencies</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {Object.entries(skills).map(([category, skillList]) => (
                            <div key={category} className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
                                <h4 className="text-xl font-bold text-slate-800 mb-4">{category}</h4>
                                <ul className="space-y-2">
                                    {skillList.map((skill, index) => (
                                        <li key={index} className="flex items-center text-slate-600">
                                            <ShieldCheck className="w-4 h-4 mr-3 text-teal flex-shrink-0" />
                                            <span>{skill}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>
                </section>

            </main>

            <footer id="contact" className="bg-slate-800 text-white mt-24 md:mt-32">
                <div className="container mx-auto px-6 py-12 text-center">
                    <h3 className="text-2xl font-bold">Get In Touch</h3>
                    <p className="mt-4 max-w-xl mx-auto text-slate-300">
                        I'm always open to discussing new projects, creative ideas, or opportunities to be part of an ambitious vision.
                    </p>
                    <div className="mt-8">
                        <a href="mailto:gainshin.hsiao@mail.mcgill.ca" className="bg-teal text-white px-8 py-3 rounded-md font-semibold hover:bg-teal-dark transition-colors inline-block">
                            Say Hello
                        </a>
                    </div>
                    <div className="mt-10 flex justify-center items-center space-x-6">
                        <a href="mailto:gainshin.hsiao@mail.mcgill.ca" className="text-slate-400 hover:text-white transition-colors">
                            <Mail className="w-6 h-6" />
                        </a>
                        <a href="https://www.linkedin.com/in/joshuahsiao" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition-colors">
                            <Linkedin className="w-6 h-6" />
                        </a>
                        <a href="https://www.youtube.com/@PrivacyUX" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition-colors">
                            <Youtube className="w-6 h-6" />
                        </a>
                    </div>
                    <div className="mt-12 border-t border-slate-700 pt-8">
                        <p className="text-slate-400 text-sm">&copy; {new Date().getFullYear()} Joshua Hsiao. All rights reserved.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
} 