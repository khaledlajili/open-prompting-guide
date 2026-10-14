import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';

import styles from './styles.module.css';

export type CardItem = {
  title: string;
  description: string;
  href: string;
  badge?: string;
  meta?: string;
  cta?: string;
};

type Props = {
  cards: readonly CardItem[];
  className?: string;
};

export function CardGrid({cards, className}: Props): ReactNode {
  return (
    <div className={clsx(styles.grid, className)}>
      {cards.map((card) => (
        <article key={card.href} className={styles.card}>
          <div className={styles.cardInner}>
            {card.badge ? <div className={styles.badge}>{card.badge}</div> : null}
            <h3 className={styles.title}>
              <Link className={styles.titleLink} to={card.href}>
                {card.title}
              </Link>
            </h3>
            <p className={styles.description}>{card.description}</p>
            {card.meta ? <p className={styles.meta}>{card.meta}</p> : null}
            <div className={styles.footer}>
              <Link className={styles.cta} to={card.href}>
                {card.cta ?? 'Open'}
              </Link>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}