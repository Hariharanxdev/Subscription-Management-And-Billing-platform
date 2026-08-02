import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { useAuth } from "../../context/AuthContext";
import Input from "../../components/ui/Input";
import PasswordInput from "../../components/ui/PasswordInput";
import Button from "../../components/ui/Button";
import { extractErrorMessage } from "../../utils/format";

export default function Register() {
  const { register: registerUser, login } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm();

  const password = watch("password");

  async function onSubmit(values) {
    try {
      await registerUser({
        username: values.username,
        email: values.email,
        password: values.password,
      });
      toast.success("Account created. Signing you in…");
      await login(values.email, values.password);
      navigate("/app/dashboard", { replace: true });
    } catch (err) {
      toast.error(extractErrorMessage(err));
    }
  }

  return (
    <div>
      <div className="mb-8">
        <p className="text-xs font-semibold uppercase tracking-wider text-ledger-500">Get started</p>
        <h2 className="mt-1.5 text-2xl font-display text-ink">Create your account</h2>
        <p className="mt-1.5 text-sm text-ink-faint">Set up billing in under a minute.</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
        <Input
          label="Username"
          autoComplete="username"
          placeholder="janedoe"
          error={errors.username?.message}
          {...register("username", {
            required: "Username is required",
            minLength: { value: 3, message: "At least 3 characters" },
            maxLength: { value: 50, message: "At most 50 characters" },
          })}
        />
        <Input
          label="Email"
          type="email"
          autoComplete="email"
          placeholder="you@example.com"
          error={errors.email?.message}
          {...register("email", {
            required: "Email is required",
            pattern: { value: /^\S+@\S+\.\S+$/, message: "Enter a valid email" },
          })}
        />
        <PasswordInput
          label="Password"
          autoComplete="new-password"
          placeholder="At least 8 characters"
          error={errors.password?.message}
          {...register("password", {
            required: "Password is required",
            minLength: { value: 8, message: "At least 8 characters" },
            maxLength: { value: 128, message: "At most 128 characters" },
          })}
        />
        <PasswordInput
          label="Confirm password"
          autoComplete="new-password"
          placeholder="Re-enter your password"
          error={errors.confirmPassword?.message}
          {...register("confirmPassword", {
            required: "Please confirm your password",
            validate: (value) => value === password || "Passwords don't match",
          })}
        />
        <Button type="submit" className="w-full" loading={isSubmitting}>
          Create account
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-ink-faint">
        Already have an account?{" "}
        <Link to="/login" className="font-medium text-ledger-600 hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  );
}
