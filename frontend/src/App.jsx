import React, { useState } from 'react';

function LabelChecker() {
  const [formData, setFormData] = useState({ brand: '', type: '', abv: '', volume: '' });
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    for (let key in formData) data.append(key, formData[key]);
    data.append('label', file);

    const res = await fetch('https://label-verification-app.onrender.com/api/check-label', {
      method: 'POST',
      body: data,
    });

    const json = await res.json();
    setResult(json);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Alcohol Label Checker</h1>
      <div className="bg-blue-50 border-l-4 border-blue-400 text-blue-800 p-4 mb-6 rounded">
        <h2 className="font-semibold text-lg mb-2">Label Entry Instructions</h2>
        <ul className="list-disc list-inside text-sm space-y-2">
          <li>
            <strong>Brand Name</strong> - The brand under which the product is sold (e.g. <em>Old Tom Distillery</em>).
          </li>
          <li>
            <strong>Product Class/Type</strong> - The general class or type of the beverage.
            For distilled spirits, this could be the designation (e.g. <em>Kentucky Straight Bourbon Whiskey</em> or <em>Vodka</em>),
            for beer it might be the style (e.g. <em>IPA</em>).
          </li>
          <li>
            <strong>Alcohol Content</strong> - The alcohol by volume (ABV) percentage
            (e.g. <em>45%</em>). You can enter this as either a percentage or just the number.
          </li>
          <li>
            <strong>Net Contents</strong> - The volume of the product (e.g. <em>750 mL</em>, <em>12 fl oz</em>).
            <span className="text-gray-600"> (Optional for minimum viable product.)</span>
          </li>
          <li>Label must include the <strong>"GOVERNMENT WARNING"</strong> statement.</li>
          <li>Use a <strong>clear, high-resolution image</strong> with good lighting (no blur or shadows).</li>
        </ul>
      </div>      
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="brand" placeholder="Brand Name" className="border p-2 w-full" onChange={handleChange} required />
        <input name="type" placeholder="Product Type" className="border p-2 w-full" onChange={handleChange} required />
        <input name="abv" placeholder="Alcohol Content (e.g. 40%)" className="border p-2 w-full" onChange={handleChange} required />
        <input name="volume" placeholder="Volume (optional)" className="border p-2 w-full" onChange={handleChange} />
        <input type="file" accept="image/*" onChange={handleFileChange} className="border p-2 w-full" required />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Submit</button>
      </form>

      {result && (
        <div className="mt-6 p-4 border rounded bg-gray-100">
          {(() => {
            const mismatches = result.details.filter(item => !item.match);
            const mismatchCount = mismatches.length;
            const allMatched = mismatchCount === 0;

            return (
              <>
                <h2 className="text-lg font-bold">
                  {allMatched
                    ? '✅ All fields matched!'
                    : `❌ ${mismatchCount} field${mismatchCount > 1 ? 's' : ''} did not match.`}
                </h2>

                {/* Warning message below summary if any field failed */}
                {!allMatched && (
                  <p className="text-yellow-600 mt-1">
                    ⚠ The quality of the label image may affect results. Please try a clearer or more complete image.
                  </p>
                )}

                {/* Bullet list of results */}
                <ul className="mt-4 list-disc ml-4 space-y-1">
                  {result.details.map((item, idx) => (
                    <li key={idx} className={item.match ? 'text-green-600' : 'text-red-600'}>
                      {item.message}
                    </li>
                  ))}
                </ul>
              </>
            );
          })()}
        </div>
      )}
    </div>
  );
}

export default LabelChecker;
