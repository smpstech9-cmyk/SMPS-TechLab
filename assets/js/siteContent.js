/**
 * SMPS Tech Lab — Centralized Site Content & Fallback Configuration
 * 
 * This file contains the default content and structure for all website sections.
 * When dynamic API or CMS data is not reachable, the site seamlessly hydrates
 * using the structured content defined here.
 * 
 * For full dynamic management, use the Admin Panel at /admin/admin.html
 */

(function () {
    'use strict';

    const SiteContent = {
        meta: {
            organization: "SMPS Tech Lab",
            tagline: "India's Premier Deep-Tech Innovation & Industrial Skilling Ecosystem",
            parentCompany: "SMPS Electric Control Pvt. Ltd.",
            established: "2026",
            address: "VTU-VRIF-TCOE Building, 1st Main Rd, RHCS Layout, Annasandraswari Nagar, Nagarabhavi, Bengaluru, Karnataka 560091",
            email: "smpstechlab@gmail.com",
            phones: ["9035874229", "8792779543"],
            hours: "10:00 AM – 8:00 PM (All days, Tuesday Holiday)",
            social: {
                linkedin: "https://www.linkedin.com/company/smpstechlab",
                instagram: "https://www.instagram.com/smpstechlab",
                twitter: "https://twitter.com/smpstechlab",
                youtube: "https://www.youtube.com/@smpstechlab"
            }
        },

        navigation: [
            { label: "Home", url: "index.html" },
            { label: "About Us", url: "about.html" },
            { label: "Products", url: "products.html" },
            { label: "IP Portfolio", url: "ip-portfolio.html" },
            { label: "Collaborate", url: "collaborate.html" },
            { label: "Execom", url: "execom.html" },
            { label: "Events", url: "events.html" },
            { label: "Gallery", url: "gallery.html" },
            { label: "Careers", url: "careers.html" },
            { label: "Contact", url: "contact.html" }
        ],

        home: {
            heroBadge: "India’s Deep-Tech R&D Ecosystem",
            heroTitle: "Enabling Future Industrial Transformation<br>Through <span>Deep-Tech Innovation</span>.",
            heroSub: "SMPS Tech Lab is a research-driven technology and innovation division of SMPS Electric Control Pvt. Ltd. focused on <span class=\"highlight\">DeepTech</span> <span class=\"highlight\">R&D</span>, Artificial Intelligence, Power Electronics, Telecom Technologies, Industrial Automation, Embedded Systems, and Advanced Product Engineering.",
            primaryBtnText: "Explore Innovations →",
            primaryBtnUrl: "products.html",
            secondaryBtnText: "Partner With Us",
            secondaryBtnUrl: "collaborate.html",
            stats: [
                { num: "50+", label: "Patents & Publications" },
                { num: "100+", label: "Industry Projects" },
                { num: "500+", label: "Engineers Trained" },
                { num: "25+", label: "Institutional Partners" }
            ],
            tickerItems: [
                "🚀 Next-Gen GaN Power Inverters Live in Prototype Testing",
                "💡 VTU-TCOE Centre of Excellence Induction Open",
                "⚡ Industrial IoT Edge Node v4.2 Released for Deployment",
                "🔬 5 Patents Filed in Deep-Tech Power Management",
                "🤝 Strategic MoUs Signed with 12 Engineering Institutions"
            ],
            ctaHead: "Your Career Starts Before <span>Your First Job</span>",
            ctaSub: "Don't wait for a placement. Build the experience that makes you un-ignorable.",
            ctaBtn: "Build Your Future Today →",
            ctaUrl: "contact.html"
        },

        about: {
            heroBadge: "About SMPS Tech Lab",
            heroTitle: "Pioneering Deeptech R&D & <span>Power Electronics Innovation</span>",
            heroSub: "SMPS Tech Lab is a center of excellence driving next-generation engineering research, prototype development, and system integration. We bridge the gap between academic theory and deeptech industrial applications through hands-on project execution.",
            vision: "To empower every student in India with the practical skills, industry confidence, and real-world experience needed to lead the global deeptech revolution.",
            mission: "To build a robust ecosystem that transforms theoretical learning into tangible, high-impact technologies through hands-on projects, industry mentorship, and cutting-edge R&D.",
            innovationLandscape: [
                {
                    id: "deeptech-rd",
                    category: "Core R&D",
                    icon: "cpu",
                    title: "Deeptech R&D",
                    desc: "Executing industrial research, prototype development, and advanced system integration suitable for power, railway, defense, space, nuclear, and energy sectors."
                },
                {
                    id: "academia-collab",
                    category: "Partnerships",
                    icon: "network",
                    title: "Academia Collaborations",
                    desc: "Partnering with universities, accelerators, OEMs, and government bodies on sponsored research projects, pilot deployments, and commercialization of indigenous technologies."
                },
                {
                    id: "tech-entrepreneurship",
                    category: "Incubation",
                    icon: "zap",
                    title: "Technical Entrepreneurship",
                    desc: "Fostering problem-solving, technology commercialization, and product innovation through ideation programs, innovation labs, and technology-driven engagements."
                },
                {
                    id: "startup-ecosystem",
                    category: "Venture",
                    icon: "rocket",
                    title: "Start-up Ecosystem",
                    desc: "Operating innovation-driven incubation-support systems, startup creation initiatives, conclaves, demo days, and proof-of-concept environments."
                },
                {
                    id: "core-platforms",
                    category: "Hardware",
                    icon: "layers",
                    title: "Deeptech Core Platforms",
                    desc: "Designing, developing, testing, and validating advanced systems in embedded electronics, power electronics, industrial automation, control networks, IoT, and AI."
                },
                {
                    id: "quantum-tech",
                    category: "Next-Gen",
                    icon: "atom",
                    title: "Quantum & Advanced Computing",
                    desc: "Driving design research and prototype manufacturing of innovative deeptech hardware and algorithms in quantum engineering, AI systems, and secure telemetry."
                },
                {
                    id: "telecom-networks",
                    category: "Connectivity",
                    icon: "radio",
                    title: "5G / 6G & Telecom Networks",
                    desc: "Pioneering high-frequency transceivers, phased-array antenna layouts, low-latency communication architectures, and licensed reference designs."
                },
                {
                    id: "esdm-advancement",
                    category: "Skilling",
                    icon: "award",
                    title: "ESDM Professional Skilling",
                    desc: "Empowering new-age engineering students, faculties, and researchers with advanced competencies for high-precision manufacturing roles in ESDM sectors."
                }
            ],
            achievements: [
                { num: "100+", label: "Live Industry Projects" },
                { num: "500+", label: "Job-Ready Engineers" },
                { num: "25+", label: "Industry Partners" },
                { num: "90%", label: "Placement Success Rate" }
            ]
        },

        execom: {
            heroTitle: "Leadership That <span>Inspires</span>",
            heroDesc: "Meet the visionaries driving SMPS Tech Lab's mission — a diverse team of industry experts, researchers, and strategic leaders committed to building India's innovation ecosystem.",
            minds: [
                {
                    id: 1,
                    name: "Suresh Kumar",
                    role: "Founder & CEO",
                    designation: "Managing Director",
                    organization: "SMPS Electric Control Pvt. Ltd.",
                    type: "execom",
                    initials: "SK",
                    img: "",
                    bio: "Visionary leader with 20+ years in power electronics, industrial automation, and technology entrepreneurship.",
                    linkedin: "https://linkedin.com",
                    email: "sureshkumar@smpstechlab.com"
                },
                {
                    id: 2,
                    name: "Dr. Priya Rao",
                    role: "Chief Research Officer",
                    designation: "Head of R&D",
                    organization: "SMPS Tech Lab",
                    type: "execom",
                    initials: "PR",
                    bio: "PhD from IIT Bombay with extensive research in AI-driven energy optimization, power switching topologies, and thermal modeling.",
                    linkedin: "https://linkedin.com",
                    email: "priyarao@smpstechlab.com"
                },
                {
                    id: 3,
                    name: "Arjun Mehta",
                    role: "VP, Strategic Alliances",
                    designation: "Vice President",
                    organization: "SMPS Tech Lab",
                    type: "execom",
                    initials: "AM",
                    bio: "Former industry technology leader driving nationwide academic alliances, government programs, and industry sponsored tracks.",
                    linkedin: "https://linkedin.com",
                    email: "arjunmehta@smpstechlab.com"
                },
                {
                    id: 4,
                    name: "Nisha Verma",
                    role: "Head of Product Engineering",
                    designation: "Principal Engineer",
                    organization: "SMPS Tech Lab",
                    type: "execom",
                    initials: "NV",
                    bio: "Serial innovator specializing in hardware reference designs, embedded edge controllers, and rapid prototyping from lab to market.",
                    linkedin: "https://linkedin.com",
                    email: "nishaverma@smpstechlab.com"
                }
            ],
            advisors: [
                {
                    id: 101,
                    name: "Prof. K. R. Sharma",
                    role: "Senior Academic Advisor",
                    designation: "Former Dean of Engineering",
                    organization: "VTU Belagavi",
                    type: "advisory",
                    initials: "KS",
                    bio: "Distinguished academician with over 35 years in curriculum innovation, sponsored research, and institutional quality frameworks.",
                    linkedin: "https://linkedin.com",
                    website: "https://vtu.ac.in"
                },
                {
                    id: 102,
                    name: "Rajesh Nambiar",
                    role: "Industrial Strategy Advisor",
                    designation: "Former Senior VP",
                    organization: "ABB Power Systems",
                    type: "advisory",
                    initials: "RN",
                    bio: "Industrialist guiding commercialization, supply chain strategy, grid-scale certifications, and enterprise scale-up.",
                    linkedin: "https://linkedin.com"
                },
                {
                    id: 103,
                    name: "Dr. Ananya Sen",
                    role: "IP & Commercialization Advisor",
                    designation: "Patent Attorney & Strategy Consultant",
                    organization: "National IP Forum",
                    type: "advisory",
                    initials: "AS",
                    bio: "Specialist in patent landscape analytics, international patent prosecution, technology transfer, and licensing agreements.",
                    linkedin: "https://linkedin.com"
                }
            ]
        },

        collaborate: {
            heroBadge: "Ecosystem Collaboration",
            heroTitle: "Partnerships Built for <span>Impact & Scale</span>",
            heroDesc: "Join forces with SMPS Tech Lab. Whether you are an academic institution seeking real-world project modules or an industry leader seeking specialized talent and co-developed prototypes, we have custom collaboration tracks.",
            successStories: [
                {
                    id: 1,
                    title: "Bharat Industries — Talent Pipeline",
                    description: "Recruited 15 freshers from our 'Power Electronics Track'. Result: Zero training time needed; students were productive from Day 1.",
                    organization: "Bharat Industries",
                    image: "https://images.unsplash.com/photo-1581092160607-ee22621dd758?q=80&w=800",
                    category: "Industry Partnership",
                    result: "100% Placement Success",
                    link: "contact.html"
                },
                {
                    id: 2,
                    title: "VTU Bridge Initiative",
                    description: "Implemented our 'Industry Bridge' module for 100 final-year students. Achieved a 40% increase in campus placement rates.",
                    organization: "VTU Research",
                    image: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=800",
                    category: "Academic Partnership",
                    result: "40% Higher Placement",
                    link: "contact.html"
                },
                {
                    id: 3,
                    title: "TechVista Solutions — Talent Scaling",
                    description: "Built a custom 'AI Implementation' track to train 20 interns specifically for TechVista's unique product stack.",
                    organization: "TechVista Solutions",
                    image: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=800",
                    category: "Startup Support",
                    result: "Trained & Hired in 3 Months",
                    link: "contact.html"
                }
            ]
        }
    };

    // Attach to global window object
    window.SiteContent = SiteContent;
})();
