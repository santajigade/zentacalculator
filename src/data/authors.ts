// Authors and reviewers. Calculator files refer to them by `id` in `author:` / `reviewer:`.
export interface Author {
  id: string; name: string; role: string; headline?: string; bio: string; photo: string;
  linkedin?: string; website?: string; expertise: string[];
  about?: { h: string; p: string }[];
}

export const AUTHORS: Author[] = [
  {
    id: 'santaji-gadepatil',
    name: 'Santaji Gadepatil',
    role: 'Founder & Editor',
    headline: 'B.E. (Electronics & Telecommunication) · Founder & Editor',
    bio: 'Santaji Gadepatil is the founder of Zenta Calculator. He works in industrial instrumentation and digital marketing, with hands-on experience in flow, level, pressure and temperature measurement. He checks the formulas, units and worked examples of every calculator before it is published.',
    photo: '/authors/santaji-gadepatil.jpg',
    linkedin: 'https://www.linkedin.com/in/santaji-gadepatil6680/',
    website: 'https://instrumentationblog.in/',
    about: [
      { h: 'Background', p: 'Santaji holds a B.E. in Electronics and Telecommunication Engineering. He has spent his career in the process instrumentation industry, working with flow meters, level transmitters, pressure gauges and temperature sensors used in water, oil and gas, chemical and power plants. He also runs Instrumentation Blog, a technical site with in-depth articles on field instruments and automation.' },
      { h: 'Why he built Zenta Calculator', p: 'Engineers and technicians repeat the same sums every day: scaling a 4 to 20 mA signal, converting a Pt100 reading, sizing a cable or a capacitor bank. Most online tools only work one way or hide the formula. Zenta Calculator solves for any value you leave blank and always shows the equation and a worked example, so results can be checked and trusted.' },
      { h: 'How every calculator is checked', p: 'Each calculator is built from a published standard or textbook equation (for example IEC 60751 for Pt100, ISO 5167 for orifice flow and IEC 60909 style methods for fault current). Before publishing, the worked examples are recalculated independently, units are tested in both metric and imperial, and the page is reviewed for clarity. Pages are updated when standards or rates change, and the last update date is shown on every page.' },
      { h: 'Contact and corrections', p: 'Found an error or want a new calculator? Use the contact page. Corrections are checked and published quickly, and suggestions from engineers in the field shape what gets built next.' },
    ],
    expertise: ['Industrial instrumentation', 'Flow, level, pressure and temperature measurement', 'Process automation', 'Digital marketing and SEO'],
  },
];

export const DEFAULT_AUTHOR = 'santaji-gadepatil';
export const authorById = (id?: string) => AUTHORS.find((a) => a.id === id);
export const authorUrl = (a: Author) => `/author/${a.id}/`;
