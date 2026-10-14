import type {ReactNode} from 'react';

import {CardGrid, type CardItem} from '@site/src/components/CardGrid';

import type {Props} from '@theme/BlogPostItems';

function formatBlogDate(date: string) {
  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(date));
}

function formatReadingTime(readingTime: number) {
  return `${Math.max(1, Math.ceil(readingTime))} min read`;
}

function toCardItem(content: Props['items'][number]['content']): CardItem {
  const {metadata} = content;
  const authors = metadata.authors.map((author) => author.name).join(', ');

  return {
    title: metadata.title,
    description: metadata.description,
    href: metadata.permalink,
    badge: 'Blog post',
    meta: `${formatBlogDate(metadata.date)} · ${formatReadingTime(metadata.readingTime)}${authors ? ` · ${authors}` : ''}`,
    cta: 'Read article',
  };
}

export default function BlogPostItems({items}: Props): ReactNode {
  return <CardGrid cards={items.map(({content}) => toCardItem(content))} />;
}