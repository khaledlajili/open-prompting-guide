import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
    markdown: {
        mermaid: true,
    },
    title: 'Open Prompting Guide',
    tagline: 'Learn to communicate effectively with AI through better prompts',
    favicon: 'img/logo.png',

    // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
    future: {
        v4: true, // Improve compatibility with the upcoming Docusaurus v4
    },

    url: 'https://khaledlajili.github.io',
    baseUrl: '/open-prompting-guide/',

    organizationName: 'khaledlajili',
    projectName: 'open-prompting-guide',

    onBrokenLinks: 'throw',

    // Even if you don't use internationalization, you can use this field to set
    // useful metadata like html lang. For example, if your site is Chinese, you
    // may want to replace "en" with "zh-Hans".
    i18n: {
        defaultLocale: 'en',
        locales: ['en'],
    },

    presets: [
        [
            'classic',
            {
                docs: {
                    sidebarPath: './sidebars.ts',
                    // Please change this to your repo.
                    // Remove this to remove the "edit this page" links.
                    editUrl:
                        'https://github.com/khaledlajili/open-prompting-guide/tree/main/',
                },
                theme: {
                    customCss: './src/css/custom.css',
                },

                gtag: {
                    trackingID: 'G-37CJXPBZTC',
                    anonymizeIP: true,
                },

            } satisfies Preset.Options,
        ],
    ],


    themeConfig: {
        colorMode: {
            respectPrefersColorScheme: true,
        },
        navbar: {
            title: 'Open Prompting Guide',
            logo: {
                alt: 'Open Prompting Guide Logo',
                src: 'img/logo.png',
            },
            items: [
                {
                    type: 'docSidebar',
                    sidebarId: 'guideSidebar',
                    position: 'left',
                    label: 'Guide',
                },
                {
                    to: '/blog',
                    label: 'Blog',
                    position: 'left',
                },
                {
                    href: 'https://github.com/khaledlajili/open-prompting-guide/pdf/Open-Prompting-Guide.pdf',
                    html: `
    <span style="display:inline-flex;align-items:center;gap:6px;">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/>
        <line x1="12" y1="15" x2="12" y2="3"/>
      </svg>
      Download PDF
    </span>
  `,
                    position: 'right',
                    className: 'header-pdf-link',
                },
                {
                    href: 'https://github.com/khaledlajili/open-prompting-guide',
                    label: 'GitHub',
                    position: 'right',
                },
            ],
        },
        footer: {
            copyright: `Copyright © ${new Date().getFullYear()} Open Prompting Guide.`,
        },
        prism: {
            theme: prismThemes.github,
            darkTheme: prismThemes.dracula,
        },
    } satisfies Preset.ThemeConfig


};

export default config;
