// Authors and reviewers. Calculator files refer to them by `id` in `author:` / `reviewer:`.
export interface Author {
  id: string; name: string; role: string; bio: string; photo: string;
  linkedin?: string; website?: string; expertise: string[];
}

export const AUTHORS: Author[] = [
  {
    id: 'santaji-gadepatil',
    name: 'Santaji Gadepatil',
    role: 'Founder & Editor',
    bio: 'Santaji Gadepatil is the founder of Zenta Calculator. He works in industrial instrumentation and digital marketing, with hands-on experience in flow, level, pressure and temperature measurement. He checks the formulas, units and worked examples of every calculator before it is published.',
    photo: '/authors/santaji-gadepatil.jpg',
    linkedin: 'https://www.linkedin.com/in/santaji-gadepatil6680/',
    expertise: ['Industrial instrumentation', 'Flow, level, pressure and temperature measurement', 'Process automation', 'Digital marketing and SEO'],
  },
];

export const DEFAULT_AUTHOR = 'santaji-gadepatil';
export const authorById = (id?: string) => AUTHORS.find((a) => a.id === id);
export const authorUrl = (a: Author) => `/author/${a.id}/`;
