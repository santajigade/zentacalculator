export interface Category { slug: string; name: string; icon: string; color: string; blurb: string; }

// Order here = order in the navigation bar.
export const CATEGORIES: Category[] = [
  { slug: 'biology', name: 'Biology', icon: '🧬', color: '#16a34a', blurb: 'Genetics, cells, growth and lab calculations.' },
  { slug: 'chemistry', name: 'Chemistry', icon: '⚗️', color: '#9333ea', blurb: 'Molarity, stoichiometry, gas laws and solutions.' },
  { slug: 'construction', name: 'Construction', icon: '🏗️', color: '#d97706', blurb: 'Concrete, bricks, paint, flooring and materials.' },
  { slug: 'conversion', name: 'Conversion', icon: '🔁', color: '#2563eb', blurb: 'Units, number systems, lakh–crore–million and more.' },
  { slug: 'ecology', name: 'Ecology', icon: '🌱', color: '#059669', blurb: 'Carbon footprint, energy use and environment.' },
  { slug: 'electrical', name: 'Electrical', icon: '🔌', color: '#ca8a04', blurb: 'Power, motors, transformers, cables, earthing and power quality.' },
  { slug: 'electronics', name: 'Electronics', icon: '🔋', color: '#0891b2', blurb: 'Circuits, LEDs, op-amps, filters, timers and converters.' },
  { slug: 'engineering', name: 'Engineering', icon: '⚙️', color: '#ea580c', blurb: 'Flow, pressure, level, temperature, instrumentation and mechanical.' },
  { slug: 'everyday-life', name: 'Everyday life', icon: '🏠', color: '#db2777', blurb: 'Time, dates, cooking, shopping and travel.' },
  { slug: 'finance', name: 'Finance', icon: '💰', color: '#0d9488', blurb: 'Loans, EMI, SIP, interest, tax and investing.' },
  { slug: 'food', name: 'Food', icon: '🍲', color: '#e11d48', blurb: 'Recipes, servings, calories and kitchen conversions.' },
  { slug: 'health', name: 'Health', icon: '❤️', color: '#dc2626', blurb: 'BMI, calories, body fat, pregnancy and fitness.' },
  { slug: 'math', name: 'Math', icon: '➗', color: '#4f46e5', blurb: 'Algebra, geometry, fractions, percentages.' },
  { slug: 'physics', name: 'Physics', icon: '⚡', color: '#0284c7', blurb: 'Mechanics, electricity, waves and thermodynamics.' },
  { slug: 'sports', name: 'Sports', icon: '🏏', color: '#65a30d', blurb: 'Run rate, pace, scores and training.' },
  { slug: 'statistics', name: 'Statistics', icon: '📊', color: '#7c3aed', blurb: 'Mean, standard deviation, probability, tests.' },
  { slug: 'other', name: 'Other', icon: '✨', color: '#64748b', blurb: 'Everything that does not fit elsewhere.' },
];

export const catBySlug = (slug: string) => CATEGORIES.find((c) => c.slug === slug);
