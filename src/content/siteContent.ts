import type {CardItem} from '@site/src/components/CardGrid';

export const guideCards: readonly CardItem[] = [
    {
        title: 'Open Prompting Guide',
        description:
            'A Practical Guide to Getting Better Results from Large Language Models',
        href: '/docs/intro',
        badge: 'Guide',
        cta: 'Read the guide',
    }
];

export const featuredBlogPosts: readonly CardItem[] = [
    {
        title: 'Why Prompt Engineering Matters for Better AI Results',
        description:
            'Prompt engineering dramatically improves the quality, reliability, and usefulness of AI outputs by carefully designing the instructions given to large language models.',
        href: '/blog/why-prompt-engineering-matters',
        badge: 'Blog',
        meta: 'October 10, 2026',
        cta: 'Read article',
    },
    {
        title: 'From Simple Instructions to Advanced Reasoning Techniques',
        description:
            'Modern prompting goes far beyond basic commands. Structured reasoning techniques such as Chain-of-Thought and ReAct significantly improve performance on complex problems.',
        href: '/blog/from-instructions-to-reasoning',
        badge: 'Blog',
        meta: 'October 13, 2026',
        cta: 'Read article',
    },
];