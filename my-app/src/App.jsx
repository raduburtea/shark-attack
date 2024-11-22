import React, { useState } from 'react';
import { Card, CardContent } from '/Users/raduburtea/Desktop/Projects/shark-attack/my-app/components/ui/card.tsx';
import { Label } from '/Users/raduburtea/Desktop/Projects/shark-attack/my-app/components/ui/label.tsx';
import { Input } from '/Users/raduburtea/Desktop/Projects/shark-attack/my-app/components/ui/input.tsx';
import { Button } from '/Users/raduburtea/Desktop/Projects/shark-attack/my-app/components/ui/button.tsx';

const InjuryForm = () => {
  const [formData, setFormData] = useState({
    country: '',
    activity: '',
    type: '',
    injury: '',
    month: ''
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/shark_attacks/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
      <div className="container mx-auto max-w-md">
        <Card className="w-full">
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              {Object.keys(formData).map((field) => (
                <div key={field} className="space-y-2">
                  <Label htmlFor={field} className="block text-sm font-medium capitalize">
                    {field}:
                  </Label>
                  <Input
                    id={field}
                    value={formData[field]}
                    onChange={(e) => handleChange(field, e.target.value)}
                    className="block w-full"
                  />
                </div>
              ))}
              <div className="pt-4">
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? 'Processing...' : 'Submit'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {results && (
          <Card className="mt-4 w-full">
            <CardContent className="p-6">
              <h2 className="mb-4 text-xl font-bold">Results</h2>
              <pre className="whitespace-pre-wrap rounded bg-gray-100 p-4">
                {JSON.stringify(results, null, 2)}
              </pre>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default InjuryForm;