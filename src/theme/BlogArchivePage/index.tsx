import type {ReactNode} from 'react';

import {CardGrid, type CardItem} from '@site/src/components/CardGrid';

import {PageMetadata} from '@docusaurus/theme-common';
import {translate} from '@docusaurus/Translate';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import type {Props} from '@theme/BlogArchivePage';

function formatBlogDate(date: string) {
  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(date));
}

function toCardItem({metadata}: Props['archive']['blogPosts'][number]): CardItem {
  const authors = metadata.authors.map((author) => author.name).join(', ');

  return {
    title: metadata.title,
    description: metadata.description,
    href: metadata.permalink,
    badge: 'Blog post',
    meta: `${formatBlogDate(metadata.date)} · ${Math.max(1, Math.ceil(metadata.readingTime))} min read${authors ? ` · ${authors}` : ''}`,
    cta: 'Read article',
  };
}

export default function BlogArchive({archive}: Props): ReactNode {
  const title = translate({
    id: 'theme.blog.archive.title',
    message: 'Archive',
    description: 'The page & hero title of the blog archive page',
  });
  const description = translate({
    id: 'theme.blog.archive.description',
    message: 'Archive',
    description: 'The page & hero description of the blog archive page',
  });

  return (
    <>
      <PageMetadata title={title} description={description} />
      <Layout>
        <header className="hero hero--primary">
          <div className="container">
            <Heading as="h1" className="hero__title">
              {title}
            </Heading>
            <p className="hero__subtitle">
              {description} {archive.blogPosts.length} posts.
            </p>
          </div>
        </header>
        <main className="margin-vert--lg">
          <div className="container">
            <CardGrid cards={archive.blogPosts.map((post) => toCardItem(post))} />
          </div>
        </main>
      </Layout>
    </>
  );
}
