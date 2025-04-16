import Head from "next/head";
import styles from "../styles/Home.module.css";

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Snippet</title>
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          NextJS with JavaScript
        </h1>

        <p className={styles.description}>
          
        </p>

        <div className={styles.grid}>
          <a 
            href="https://github.com/ptbdnr/snippets" 
            target="_blank" 
            className={styles.card}
          >
            <h3>Documentation &rarr;</h3>
            <p>Find the documentation and learn more.</p>
          </a>

          <a
            href="https://github.com/vercel/next.js/tree/canary/examples"
            target="_blank"
            className={styles.card}
          >
            <h3>NextJS Examples &rarr;</h3>
            <p>Discover and deploy boilerplate example Next.js projects.</p>
          </a>

        </div>
      </main>

      <footer className={styles.footer}>
        Made with ❤️ by ptbdnr
      </footer>
    </div>
  );
}
