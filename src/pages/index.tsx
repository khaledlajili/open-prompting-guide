import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import {CardGrid} from '@site/src/components/CardGrid';
import {
    featuredBlogPosts,
    guideCards,
} from '@site/src/content/siteContent';

import styles from './index.module.css';

function HomepageHeader() {
    const {siteConfig} = useDocusaurusContext();
    return (
        <header className={styles.heroBanner}>
            <div className={clsx('container', styles.heroContent)}>
                <p className={styles.eyebrow}>Democratizing prompting knowledge</p>
                <Heading as="h1" className={styles.heroTitle}>
                    {siteConfig.title}
                </Heading>
                <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
                <p className={styles.heroBody}>
                    A Practical Guide to Getting Better Results from Large Language Models
                </p>
                <div className={styles.buttons}>
                    <Link className="button button--primary button--lg" to="/docs/intro">
                        Browse guide
                    </Link>
                    <Link className="button button--secondary button--lg" to="/blog">
                        Read the blog
                    </Link>
                </div>
            </div>
        </header>
    );
}

function SectionHeader({
                           title,
                           description,
                           href,
                           linkLabel,
                       }: {
    title: string;
    description: string;
    href: string;
    linkLabel: string;
}) {
    return (
        <div className={styles.sectionHeader}>
            <div>
                <p className={styles.sectionKicker}>{description}</p>
                <Heading as="h2" className={styles.sectionTitle}>
                    {title}
                </Heading>
            </div>
            <Link className={styles.sectionLink} to={href}>
                {linkLabel}
            </Link>
        </div>
    );
}

export default function Home(): ReactNode {
    const {siteConfig} = useDocusaurusContext();

    return (
        <Layout
            description="A practical guide with prompting publications and blog updates.">
            <HomepageHeader />
            <main className={styles.homepageMain}>
                <section className={styles.section}>
                    <div className="container">
                        <SectionHeader
                            title="Open Prompting Guide"
                            description="Deep dives into prompting, AI agents, and more."
                            href="/docs/intro"
                            linkLabel="Browse the guide"
                        />
                        <CardGrid cards={guideCards.slice(0, 3)} />
                    </div>
                </section>

                <section className={styles.section}>
                    <div className="container">
                        <SectionHeader
                            title="Recent blog posts"
                            description="Announcements, technical notes, and evolving thoughts around prompting."
                            href="/blog"
                            linkLabel="Browse all posts"
                        />
                        <CardGrid cards={featuredBlogPosts} />
                    </div>
                </section>
            </main>
        </Layout>
    );
}
