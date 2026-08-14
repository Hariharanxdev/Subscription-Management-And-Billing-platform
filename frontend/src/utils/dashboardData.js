export function getSubscriptionPlanName(subscription) {
  if (!subscription) return 'Unknown plan';

  if (subscription.plan?.plan_name) {
    return subscription.plan.plan_name;
  }

  if (subscription.plan_name) {
    return subscription.plan_name;
  }

  return 'Unknown plan';
}
