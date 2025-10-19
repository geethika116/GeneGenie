import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Rocket } from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="max-w-2xl w-full p-8">
        <div className="flex flex-col items-center text-center gap-6">
          <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
            <Rocket className="h-8 w-8 text-primary" />
          </div>
          
          <div className="space-y-2">
            <h1 className="text-3xl font-semibold text-foreground" data-testid="text-title">
              Fullstack JavaScript Template
            </h1>
            <p className="text-muted-foreground" data-testid="text-description">
              A clean starting point for your next project
            </p>
          </div>

          <div className="flex flex-col gap-3 w-full max-w-sm">
            <div className="text-sm text-muted-foreground space-y-1">
              <p>✓ React + TypeScript frontend</p>
              <p>✓ Express backend with API routes</p>
              <p>✓ Shadcn UI components</p>
              <p>✓ Dark mode support</p>
              <p>✓ TanStack Query for data fetching</p>
            </div>
          </div>

          <Button 
            data-testid="button-get-started"
            onClick={() => console.log('Get started clicked')}
          >
            Get Started
          </Button>
        </div>
      </Card>
    </div>
  );
}
