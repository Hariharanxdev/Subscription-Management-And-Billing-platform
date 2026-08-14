import test from 'node:test';
import assert from 'node:assert/strict';
import { getSubscriptionPlanName } from './dashboardData.js';

test('returns the nested plan name when available', () => {
  assert.equal(getSubscriptionPlanName({ plan: { plan_name: 'Pro' } }), 'Pro');
});

test('falls back to a top-level plan name when present', () => {
  assert.equal(getSubscriptionPlanName({ plan_name: 'Enterprise' }), 'Enterprise');
});

test('returns a safe fallback when no plan data exists', () => {
  assert.equal(getSubscriptionPlanName({}), 'Unknown plan');
});
