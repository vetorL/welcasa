import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, Building2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PropertyTable, Property } from "@/components/PropertyTable";
import { PropertyModal } from "@/components/PropertyModal";
import { propertyService } from "@/services/propertyService";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProperty, setEditingProperty] = useState<Property | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const { data: properties = [], isLoading } = useQuery({
    queryKey: ["properties"],
    queryFn: propertyService.getAll,
  });

  const createMutation = useMutation({
    mutationFn: propertyService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["properties"] });
      setModalOpen(false);
      toast({
        title: "Sucesso!",
        description: "Imóvel cadastrado com sucesso",
      });
    },
    onError: () => {
      toast({
        title: "Erro",
        description: "Não foi possível cadastrar o imóvel",
        variant: "destructive",
      });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Omit<Property, "id"> }) =>
      propertyService.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["properties"] });
      setModalOpen(false);
      setEditingProperty(null);
      toast({
        title: "Sucesso!",
        description: "Imóvel atualizado com sucesso",
      });
    },
    onError: () => {
      toast({
        title: "Erro",
        description: "Não foi possível atualizar o imóvel",
        variant: "destructive",
      });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: propertyService.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["properties"] });
      toast({
        title: "Sucesso!",
        description: "Imóvel removido com sucesso",
      });
    },
    onError: () => {
      toast({
        title: "Erro",
        description: "Não foi possível remover o imóvel",
        variant: "destructive",
      });
    },
  });

  const handleSubmit = (data: Omit<Property, "id">) => {
    if (editingProperty) {
      updateMutation.mutate({ id: editingProperty.id, data });
    } else {
      createMutation.mutate(data);
    }
  };

  const handleEdit = (property: Property) => {
    setEditingProperty(property);
    setModalOpen(true);
  };

  const handleDelete = (id: number) => {
    if (window.confirm("Tem certeza que deseja remover este imóvel?")) {
      deleteMutation.mutate(id);
    }
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setEditingProperty(null);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Building2 className="h-8 w-8 text-accent" />
              <div>
                <h1 className="text-3xl font-extrabold text-primary">
                  Welcasa
                </h1>
                <p className="text-sm text-muted-foreground">
                  Gestão de Imóveis
                </p>
              </div>
            </div>
            <Button
              onClick={() => setModalOpen(true)}
              className="bg-accent hover:bg-accent/90 gap-2"
            >
              <Plus className="h-5 w-5" />
              Novo Imóvel
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-primary mb-2">
            Lista de Imóveis
          </h2>
          <p className="text-muted-foreground">
            Gerencie todos os seus imóveis cadastrados na plataforma
          </p>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Carregando imóveis...</p>
          </div>
        ) : (
          <PropertyTable
            properties={properties}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        )}
      </main>

      {/* Modal */}
      <PropertyModal
        open={modalOpen}
        onOpenChange={handleCloseModal}
        property={editingProperty}
        onSubmit={handleSubmit}
        isLoading={createMutation.isPending || updateMutation.isPending}
      />
    </div>
  );
};

export default Index;
