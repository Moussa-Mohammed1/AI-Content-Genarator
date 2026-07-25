import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-[90vh] flex flex-col">
      <section className="flex-1 flex items-center justify-center px-4 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6">
            AI-Powered{" "}
            <span className="text-indigo-600">Content Generation</span>
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            Create high-quality blog posts, social media content, ads, emails,
            and more with the power of AI. Save time and scale your content
            strategy.
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link
              href="/register"
              className="bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition"
            >
              Get Started Free
            </Link>
            <Link
              href="/login"
              className="text-gray-600 px-8 py-3 rounded-lg text-lg font-semibold border hover:bg-gray-50 transition"
            >
              Sign In
            </Link>
          </div>
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { label: "Content Types", value: "12+" },
              { label: "AI Models", value: "5" },
              { label: "Export Formats", value: "5" },
              { label: "SEO Tools", value: "Built-in" },
            ].map((stat) => (
              <div key={stat.label} className="bg-white rounded-xl p-6 shadow-sm">
                <div className="text-2xl font-bold text-indigo-600">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-500 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
      <section className="bg-white py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">
            Everything you need to create content
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: "Blog Posts",
                desc: "Generate engaging, SEO-optimized blog content",
              },
              {
                title: "Social Media",
                desc: "Create platform-specific posts that engage",
              },
              {
                title: "Ads & Emails",
                desc: "High-converting copy for campaigns",
              },
              {
                title: "Landing Pages",
                desc: "Conversion-optimized page content",
              },
              {
                title: "SEO Metadata",
                desc: "Titles, descriptions, and keywords",
              },
              {
                title: "Rich Editor",
                desc: "Edit, rewrite, and polish with AI tools",
              },
            ].map((feature) => (
              <div
                key={feature.title}
                className="p-6 rounded-xl border hover:shadow-md transition"
              >
                <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                <p className="text-gray-600 text-sm">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
