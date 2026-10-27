import { test } from 'node:test';
import assert from 'node:assert/strict';
import { compile } from '../src/lib/expr.ts';
import { compileAll, solve } from '../src/lib/solver.ts';

const close = (a: number, b: number, tol = 1e-6) => assert.ok(Math.abs(a - b) <= tol * Math.max(1, Math.abs(b)), `${a} != ${b}`);

test('parser precedence', () => {
  close(compile('2 + 3 * 4 ^ 2').fn({}), 50);
  close(compile('-2^2').fn({}), -4);
  close(compile('2^3^2').fn({}), 512);
  close(compile('sqrt(x) * pi').fn({ x: 4 }), 2 * Math.PI);
});

test('ohms law: any two give the rest', () => {
  const eqs = compileAll(['V = I * R', 'P = V * I']);
  const vars = ['V', 'I', 'R', 'P'];
  let r = solve(eqs, { V: 12, R: 4 }, vars);
  close(r.values.I, 3); close(r.values.P, 36);
  r = solve(eqs, { P: 100, R: 25 }, vars, { I: { min: 0 }, V: { min: 0 } });
  close(r.values.I, 2); close(r.values.V, 50);
  r = solve(eqs, { P: 60, V: 230 }, vars);
  close(r.values.R, 230 * 230 / 60);
});

test('compound interest: solve for rate and time numerically', () => {
  const eqs = compileAll(['A = P * (1 + r/n)^(n*t)']);
  const vars = ['A', 'P', 'r', 'n', 't'];
  let r = solve(eqs, { P: 1000, r: 0.08, n: 12, t: 10 }, vars);
  close(r.values.A, 1000 * (1 + 0.08 / 12) ** 120);
  r = solve(eqs, { P: 1000, A: 2000, n: 1, t: 10 }, vars, { r: { min: 0 } });
  close(r.values.r, 2 ** 0.1 - 1);
  r = solve(eqs, { P: 1000, A: 2000, n: 4, r: 0.07 }, vars);
  close(r.values.t, Math.log(2) / (4 * Math.log(1 + 0.07 / 4)));
});

test('bmi: solve height', () => {
  const eqs = compileAll(['bmi = m / h^2']);
  const r = solve(eqs, { bmi: 22, m: 70 }, ['bmi', 'm', 'h'], { h: { min: 0 } });
  close(r.values.h, Math.sqrt(70 / 22));
});

test('pole is not a root', () => {
  const eqs = compileAll(['y = 1 / x']);
  const r = solve(eqs, { y: 0 }, ['x', 'y']);
  assert.equal(r.unsolved.length, 1);
});

test('inconsistent detection', () => {
  const eqs = compileAll(['a = b * 2']);
  const r = solve(eqs, { a: 3, b: 2 }, ['a', 'b']);
  assert.deepEqual(r.inconsistent, ['a = b * 2']);
});

test('new functions', () => {
  close(compile('fact(5)').fn({}), 120);
  close(compile('nCr(10, 3)').fn({}), 120);
  close(compile('nPr(10, 3)').fn({}), 720);
  close(compile('normcdf(1.96)').fn({}), 0.9750021, 1e-6);
  close(compile('mod(-1, 24)').fn({}), 23);
  close(compile('gamma(0.5)').fn({}), Math.sqrt(Math.PI), 1e-9);
});

test('calendar functions', () => {
  const day = (s: string) => Date.parse(s + 'T00:00:00Z') / 86400000;
  close(compile('yearsBetween(a, b)').fn({ a: day('1990-03-15'), b: day('2026-03-14') }), 35);
  close(compile('yearsBetween(a, b)').fn({ a: day('1990-03-15'), b: day('2026-03-15') }), 36);
  close(compile('monthsBetween(a, b)').fn({ a: day('2026-01-31'), b: day('2026-03-01') }), 1);
  close(compile('workdays(a, b)').fn({ a: day('2026-10-26'), b: day('2026-11-02') }), 5);
  close(compile('weekday(a)').fn({ a: day('2026-10-27') }), 2);
});

test('exact combinatorics and tolerant rounding', () => {
  assert.equal(compile('nCr(49, 6)').fn({}), 13983816);
  assert.equal(compile('nPr(20, 3)').fn({}), 6840);
  assert.equal(compile('ceil(2.7 / 0.18)').fn({}), 15);
  assert.equal(compile('floor(0.29 * 100)').fn({}), 29);
});
